import base64
from typing import List, Union

from domain.dtos.plantilla_dto import PlantillaOutShortDTO, PlantillaOutDTO, SubirPlantillaDTO, \
    CambiarWordDTO
from services.files_converter_client import FileConverterClient
from services.files_service import FileService
from services.plantillas_service import PlantillasService
from services.word_replacer_service import WordReplacerService
from settings.config import logger


class PlantillasFacade:
    def __init__(self, plantillas_service: PlantillasService, replacer_service : WordReplacerService, files_service : FileService,
                 files_converter_client: FileConverterClient):
        self.plantillas_service = plantillas_service
        self.files_service = files_service
        self.replacer_service = replacer_service
        self.files_converter_client = files_converter_client

    def remplazar(self, data: CambiarWordDTO) -> Union[str, bytes]:
        archivo_docx_bytes = self.files_service.base64_a_bytes(b64=data.archivo)
        base64nuevo = self.replacer_service.reemplazar_placeholder_word(archivo_docx=archivo_docx_bytes, metadata=data.metadata, formato='base64')
        return base64nuevo

    def remplazar_y_devolver_pdf(self, data: CambiarWordDTO, devolver_en_base64: bool = False) -> Union[str, bytes]:
        """
        1) Decodifica el DOCX base64.
        2) Reemplaza placeholders -> DOCX en bytes (formato='file').
        3) Llama a file-converter-service y obtiene el PDF en bytes.
        4) Devuelve bytes o base64 del PDF según 'devolver_en_base64'.
        """
        # 1) DOCX original (bytes)
        archivo_docx_bytes = self.files_service.base64_a_bytes(b64=data.archivo)

        # 2) DOCX con placeholders reemplazados -> en BYTES
        #    (cambiado de formato='base64' a formato='file')
        docx_reemplazado_bytes = self.replacer_service.reemplazar_placeholder_word(
            archivo_docx=archivo_docx_bytes,
            metadata=data.metadata,
            formato="file"
        )

        # 3) Convertir a PDF llamando al servicio externo
        pdf_bytes = self.files_converter_client.convertir_word_to_pdf(
            docx_bytes=docx_reemplazado_bytes
        )

        # 4) Salida
        if devolver_en_base64:
            return base64.b64encode(pdf_bytes).decode("ascii")
        return pdf_bytes

    def agregar_plantilla(self, data: SubirPlantillaDTO) -> str:
        archivo_bytes = self.files_service.base64_a_bytes(data.archivo)
        data.archivo = ""

        id_usuario = "SACARLO DEL JWT CUANDO ESTE"
        nombre_usuario = "SACARLO DEL JWT CUANDO ESTE"
        hashSha256 = self.files_service.sha256_hex(archivo_bytes)
        tamano = self.files_service.tamano_bytes(archivo_bytes)
        nuevo_id,ubicacion_obs = self.plantillas_service.agregar_plantilla(data,hashSha256,tamano,id_usuario,nombre_usuario)
        return nuevo_id

    def obtener_plantilla_por_id(self, id: str) -> PlantillaOutDTO:
        model = self.plantillas_service.obtener_por_id(id)
        return PlantillaOutDTO.from_model(model)

    def eliminar_plantilla(self, id: str) -> str:
        model = self.plantillas_service.obtener_por_id(id)
        logger.info(model.ubicacionObs)

        #Eliminar registro de la base de datos
        self.plantillas_service.eliminar_plantilla(id)
        return id

    def filtrar_plantillas(self, **filtros) -> List[PlantillaOutShortDTO]:
        plantillas = self.plantillas_service.filtrar_plantillas(**filtros)
        return [PlantillaOutShortDTO.from_model(plantilla) for plantilla in plantillas]

