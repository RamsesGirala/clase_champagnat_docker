from typing import Optional
from fastapi import APIRouter, UploadFile, File, Request, Query
from fastapi.responses import StreamingResponse
from facades.files_converter_facade import FilesConverterFacade
from settings.config import logger


def get_files_converter_router(facade: FilesConverterFacade) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/convertir_word_to_pdf",
        summary="Convierte un DOCX a PDF",
        responses={200: {"content": {"application/pdf": {}}}},
    )
    async def convertir_word_to_pdf(
        request: Request,
        file: Optional[UploadFile] = File(
            default=None,
            description="DOCX vía multipart/form-data en el campo 'file'",
        ),
        filename: Optional[str] = Query(
            default=None,
            description="Nombre sugerido para el PDF de salida (sin extensión)",
        ),
    ):
        logger.info("EJECUTANDO CONVERTIR WORD A PDF")

        # Header tal como llegó
        content_type = (request.headers.get("content-type") or "").lower()

        # ¿Es multipart?
        is_multipart = (file is not None) or ("multipart/form-data" in content_type)

        # Leer bytes + metadata
        if is_multipart and file is not None:
            docx_bytes = await file.read()
            original_filename = file.filename or ""
        else:
            # modo octet-stream / raw body
            docx_bytes = await request.body()
            original_filename = ""

        # Delegar en el facade (pasamos también el flag is_multipart)
        pdf_bytes, out_name = facade.convertir_word_a_pdf(
            archivo_docx=docx_bytes,
            content_type=content_type,
            original_filename=original_filename,
            suggested_filename=filename,
            is_multipart=is_multipart,
        )

        return StreamingResponse(
            content=iter([pdf_bytes]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{out_name}"',
                "Content-Length": str(len(pdf_bytes)),
            },
        )

    return router