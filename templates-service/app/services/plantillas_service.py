from typing import List

from domain.dtos.plantilla_dto import SubirPlantillaDTO
from domain.models.plantilla_model import PlantillaModel
from exceptions.tributarios_exception import TributarioException
from repositories.plantillas_repository import PlantillasRepository


class PlantillasService:
    def __init__(self, repository: PlantillasRepository):
        self.repository = repository

    def agregar_plantilla(self, data : SubirPlantillaDTO, hashSha256: str, tamanoBytes: int,
                                subido_id: str, subido_nombre: str) -> tuple[str,str]:
        try:
            nueva_plantilla = PlantillaModel(
                nombre_archivo=data.nombre_archivo,
                nombre=data.nombre,
                descripcion=data.descripcion,
                tipo=data.tipo,
                juzgado=data.juzgado,
                hashSha256=hashSha256,
                tamanoBytes=tamanoBytes,
                subidoPorId=subido_id,
                subidoPorNombre=subido_nombre
            )
        except ValueError as e:
            raise TributarioException(
                mensaje=str(e)
            )

        self.repository.crear_plantilla(nueva_plantilla)
        return nueva_plantilla.id, nueva_plantilla.ubicacionObs

    def revertir_agregar_plantilla(self, id : str):
        self.repository.eliminar_por_id(id)

    def obtener_por_id(self, id: str) -> PlantillaModel:
        return self.repository.obtener_por_id(id)

    def eliminar_plantilla(self, id: str):
        self.repository.eliminar_por_id(id)

    def filtrar_plantillas(self, **filtros) -> List[PlantillaModel]:
        return self.repository.filtrar(**filtros)