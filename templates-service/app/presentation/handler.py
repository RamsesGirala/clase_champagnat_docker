from fastapi import Request
from fastapi.responses import JSONResponse
from settings.config import logger
from domain.dtos.plantilla_dto import BaseResponseDTO
from exceptions.tributarios_exception import TributarioException

def tributario_exception_handler(request: Request, exc: TributarioException):
    logger.info(f"[ERROR] Excepción controlada en {request.url.path}")
    logger.info(f"[MSG] {exc.mensaje}")
    return JSONResponse(
        status_code=500,
        content=BaseResponseDTO(
            error=True,
            mensaje=exc.mensaje,
            data=None
        ).model_dump()
    )

def global_exception_handler(request: Request, exc: Exception):
    logger.info(f"[ERROR] Excepción no controlada en {request.url.path}")
    logger.info(f"{exc}")

    # Default: error no manejado
    return JSONResponse(
        status_code=500,
        content=BaseResponseDTO(
            error=True,
            mensaje="ERROR NO ESPERADO, CONTACTE A SOPORTE",
            data=None
        ).model_dump()
    )
