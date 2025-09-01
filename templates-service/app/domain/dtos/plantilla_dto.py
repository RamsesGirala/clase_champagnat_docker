from datetime import datetime

from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

from domain.models.plantilla_model import PlantillaModel

# Tipo genérico para respuestas
T = TypeVar("T")

class BaseResponseDTO(BaseModel, Generic[T]):
    error: bool = False
    mensaje: Optional[str] = ""
    data: Optional[T] = None

## DTO para remplazar la metadata en un word
class CambiarWordDTO(BaseModel):
    archivo: str
    metadata: dict

## Dto para query de filtracion de plantillas
class FiltroPlantillasDTO(BaseModel):
    juzgado: Optional[str] = None
    tipo: Optional[str] = None
    texto: Optional[str] = None
    fechaDesde: Optional[datetime] = None
    fechaHasta: Optional[datetime] = None

## DTO para subir una plantilla nueva
class SubirPlantillaDTO(BaseModel):
    archivo: str
    nombre: str
    nombre_archivo: str
    descripcion: Optional[str] = None
    tipo: str
    juzgado: str

## DTO para mostrar informacion reducida de la plantilla cuando se buscan
class PlantillaOutShortDTO(BaseModel):
    id: str
    nombre: str
    tipo: str
    juzgado: str
    fechaSubida: datetime

    @classmethod
    def from_model(cls, model: "PlantillaModel") -> "PlantillaOutShortDTO":
        return cls(
            id=model.id,
            nombre=model.nombre,
            tipo=model.tipo,
            juzgado=model.juzgado,
            fechaSubida=model.fechaSubida,
        )

## DTO para mostrar toda la informacion de la plantilla
class PlantillaOutDTO(BaseModel):
    id: str
    nombre: str
    descripcion: Optional[str] = None
    tipo: str
    juzgado: str
    ubicacionObs: str
    tamanoBytes: int
    hashSha256: str
    subidoPorId: str
    subidoPorNombre: str
    fechaSubida: datetime

    @classmethod
    def from_model(cls, model: "PlantillaModel") -> "PlantillaOutDTO":
        return cls(
            id=model.id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            tipo=model.tipo,
            juzgado=model.juzgado,
            ubicacionObs=model.ubicacionObs,
            tamanoBytes=model.tamanoBytes,
            hashSha256=model.hashSha256,
            subidoPorId=model.subidoPorId,
            subidoPorNombre=model.subidoPorNombre,
            fechaSubida=model.fechaSubida,
        )
