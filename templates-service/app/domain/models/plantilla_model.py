import re
import uuid
import unicodedata
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

def _slugify_nombre(nombre: str, max_len: int = 80) -> str:
    # Normaliza acentos → ASCII
    n = unicodedata.normalize("NFKD", nombre)
    n = n.encode("ascii", "ignore").decode("ascii")
    # Minúsculas, reemplaza espacios por guiones
    n = n.lower().strip().replace(" ", "-")
    # Deja solo [a-z0-9-_]
    n = re.sub(r"[^a-z0-9\-_]", "", n)
    # Colapsa guiones múltiples
    n = re.sub(r"-{2,}", "-", n).strip("-")
    # Limita longitud
    n = n[:max_len] if len(n) > max_len else n
    return n or "plantilla"

class PlantillaModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    nombre: str
    nombre_archivo: str
    descripcion: Optional[str] = None
    tipo: str
    juzgado: str

    ubicacionObs: Optional[str] = None  # ← se autogenera
    tamanoBytes: int
    hashSha256: str

    subidoPorId: str
    subidoPorNombre: str
    fechaSubida: datetime = Field(default_factory=datetime.now)

    # =========================
    # Validadores de campos
    # =========================
    @field_validator('nombre', 'nombre_archivo','tipo', 'juzgado', 'hashSha256', 'subidoPorId', 'subidoPorNombre')
    @classmethod
    def no_cadenas_vacias(cls, v, field):
        if not isinstance(v, str) or not v.strip():
            raise ValueError(f"El campo '{field.field_name}' no puede ser vacío.")
        return v.strip()

    @field_validator('tamanoBytes')
    @classmethod
    def validar_tamano_positivo(cls, v):
        if v <= 0:
            raise ValueError("El campo 'tamanoBytes' debe ser mayor que 0.")
        return v

    @field_validator('hashSha256')
    @classmethod
    def validar_hash_sha256(cls, v):
        # 64 chars hex para SHA-256
        if not re.fullmatch(r'^[a-fA-F0-9]{64}$', v):
            raise ValueError("El campo 'hashSha256' debe ser un SHA-256 hexadecimal de 64 caracteres.")
        return v.lower()

    # =========================
    # Autogeneración de rutaGcs
    # =========================
    @model_validator(mode="after")
    def autogenerar_ruta_obs(self):
        if not self.ubicacionObs or not self.ubicacionObs.strip():
            base = _slugify_nombre(self.nombre)
            filename = f"{base}.docx"
            self.ubicacionObs = f"templates/{self.id}/{filename}"
        return self