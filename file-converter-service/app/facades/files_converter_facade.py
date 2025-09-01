import re
from typing import Optional, Tuple

from exceptions.tributarios_exception import TributarioException
from services.word_to_pdf_converter_service import WordToPdfConverterService



class FilesConverterFacade:
    def __init__(self, word_to_pdf_service: WordToPdfConverterService):
        self.word_to_pdf_service = word_to_pdf_service

    def convertir_word_a_pdf(
        self,
        archivo_docx: bytes,
        content_type: Optional[str],
        original_filename: Optional[str],
        suggested_filename: Optional[str],
        is_multipart: bool = False,
    ) -> Tuple[bytes, str]:

        ct = (content_type or "").lower()
        is_octet = ct.startswith("application/octet-stream")

        # Content-Type/forma soportada: multipart (si FastAPI parseó archivo) o application/octet-stream
        if not (is_multipart or is_octet):
            raise TributarioException(
                "Content-Type no soportado. Use multipart/form-data o application/octet-stream."
            )

        # No vacío
        if not archivo_docx:
            raise TributarioException("No se pudo convertir: el archivo vino vacío.")

        # Determinar nombre de salida
        out_name = self._build_output_filename(suggested_filename, original_filename)

        # Convertir
        pdf_bytes = self.word_to_pdf_service.convertir_docx_a_pdf(archivo_docx=archivo_docx)
        return pdf_bytes, out_name


    # ----------------- helpers -----------------
    @staticmethod
    def _build_output_filename(suggested: Optional[str], original: Optional[str]) -> str:
        """
        Prioridad:
          1) suggested (query param, sin extensión)
          2) stem de original (si viene de multipart)
          3) 'archivo'
        """
        stem = (suggested or (original.rsplit(".", 1)[0] if original else "") or "archivo").strip()
        stem = re.sub(r'[\\/*?:"<>|]+', "_", stem).replace("\n", "_").replace("\r", "_")
        stem = stem or "archivo"
        return f"{stem}.pdf"
