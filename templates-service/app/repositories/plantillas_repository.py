from typing import List, Dict, Any
from pymongo.collection import Collection

from domain.models.plantilla_model import PlantillaModel
from exceptions.tributarios_exception import TributarioException
from settings.config import logger


class PlantillasRepository:

    def __init__(self, collection: Collection):
        self.collection = collection

    def crear_plantilla(self, plantilla: PlantillaModel) -> None:
        self.collection.insert_one(plantilla.model_dump())

    def obtener_por_id(self, id: str) -> PlantillaModel:
        data = self.collection.find_one({"id": id})
        if not data:
            self.disparar_error_no_existe_plantilla(id)
        return PlantillaModel(**data)

    def eliminar_por_id(self, id: str) -> None:
        result = self.collection.delete_one({"id": id})
        if result.deleted_count == 0:
            logger.warn(f"no se borro nada de la base pq no existia la plantilla con id {id}")

    def filtrar(self, **filtros) -> List[PlantillaModel]:
        """
        Retorna una lista de plantillas que cumplan los filtros.
        - juzgado: igualdad exacta (case-sensitive por defecto en Mongo)
        - tipo: igualdad exacta
        - texto: busca en nombre o descripcion (regex case-insensitive)
        - fechaDesde/fechaHasta: rango sobre fechaSubida (inclusive)
        """

        juzgado = filtros.get('juzgado')
        tipo = filtros.get('tipo')
        texto = filtros.get('texto')
        fechaDesde = filtros.get('fechaDesde')
        fechaHasta = filtros.get('fechaHasta')


        query: Dict[str, Any] = {}

        if juzgado:
            query["juzgado"] = juzgado

        if tipo:
            query["tipo"] = tipo

        if texto:
            # Búsqueda simple con regex en nombre o descripcion
            query["$or"] = [
                {"nombre": {"$regex": texto, "$options": "i"}},
                {"descripcion": {"$regex": texto, "$options": "i"}},
            ]

        if fechaDesde or fechaHasta:
            rango: Dict[str, Any] = {}
            if fechaDesde:
                rango["$gte"] = fechaDesde
            if fechaHasta:
                rango["$lte"] = fechaHasta
            query["fechaSubida"] = rango

        cursor = self.collection.find(query).sort("fechaSubida", -1)

        return [PlantillaModel(**doc) for doc in cursor]

    def disparar_error_no_existe_plantilla(self, id: str):
        raise TributarioException(
            mensaje=f"No existe la plantilla {id} en la base de datos"
        )
