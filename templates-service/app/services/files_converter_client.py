import requests
from typing import Optional

from settings.config import settings, logger


class FileConverterClient:
    """
    Cliente sincrónico para consumir /convertir_word_to_pdf del file-converter-service.
    """

    def __init__(self, timeout: int = 60):
        self.base_url = settings.file_converter_base_url
        self.timeout = timeout

    def convertir_word_to_pdf(self, docx_bytes: bytes, filename: Optional[str] = None) -> bytes:
        logger.info("dentro del cliente para hacer llamada al files-converter-service")

        """
        Envía un DOCX por multipart/form-data al endpoint y devuelve los bytes del PDF.
        - filename: nombre sugerido (sin .pdf); el servicio lo usa para Content-Disposition.
        """
        url = f"{self.base_url}/archivos/api/convertir_word_to_pdf"
        params = {}
        if filename:
            params["filename"] = filename

        files = {
            # campo debe llamarse 'file' (así lo espera tu endpoint)
            "file": (
                (filename or "documento") + ".docx",
                docx_bytes,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        }

        try:
            resp = requests.post(url, params=params, files=files, timeout=self.timeout)
        except requests.RequestException as ex:
            # Podés mapearlo a tu excepción de dominio
            raise RuntimeError(f"Error conectando a file-converter-service: {ex}") from ex

        if resp.status_code != 200:
            # Trae texto por si hay detalle en HTML/JSON
            raise RuntimeError(
                f"Conversión a PDF falló ({resp.status_code}): {resp.text[:500]}"
            )

        return resp.content  # bytes del PDF
