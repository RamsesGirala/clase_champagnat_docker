from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

# Tipo genérico para respuestas
T = TypeVar("T")

class BaseResponseDTO(BaseModel, Generic[T]):
    error: bool = False
    mensaje: Optional[str] = ""
    data: Optional[T] = None

# DTO que se encola a la cola de plantillas ya convertidas a pdf
class PlantillaConvertidaDTO(BaseModel):
    job_id: str
    lote_id: str
    demanda_id: str
    ubicacion_obs: str
    usuario_id: str
    actuacion_tipo: str
    actuacion_descripcion: str
    plantilla_nombre: str

# DTO que se desencola de la cola de plantillas a convertir de word a pdf
class PlantillaConvertirDTO(BaseModel):
    job_id: str
    lote_id: str
    demanda_id: str
    ubicacion_obs: str
    usuario_id: str
    actuacion_tipo: str
    actuacion_descripcion: str
    plantilla_nombre: str
