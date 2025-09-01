from typing import List, Optional

from fastapi import APIRouter,Depends
from starlette.responses import StreamingResponse

from domain.dtos.plantilla_dto import BaseResponseDTO, PlantillaOutShortDTO, FiltroPlantillasDTO, SubirPlantillaDTO, PlantillaOutDTO, CambiarWordDTO
from facades.plantillas_facade import PlantillasFacade


def get_plantillas_router(facade: PlantillasFacade) -> APIRouter:
    router = APIRouter()

    @router.post("/", response_model=BaseResponseDTO[str])
    def agregar_plantilla(data: SubirPlantillaDTO):
        nuevo_id = facade.agregar_plantilla(data)
        return BaseResponseDTO[str](error=False, data=nuevo_id)

    @router.delete("/{id}", response_model=BaseResponseDTO)
    def eliminar_plantilla(id: str):
        facade.eliminar_plantilla(id)
        return BaseResponseDTO(error=False, data=None)

    @router.get("/buscar_plantillas", response_model=BaseResponseDTO[List[PlantillaOutShortDTO]])
    def buscar_plantillas(filtros: FiltroPlantillasDTO = Depends()):
        resultados = facade.filtrar_plantillas(**filtros.model_dump(exclude_none=True))
        return BaseResponseDTO[List[PlantillaOutShortDTO]](error=False, data=resultados)

    @router.get("/{id}", response_model=BaseResponseDTO[PlantillaOutDTO])
    def obtener_plantilla(id: str):
        data = facade.obtener_plantilla_por_id(id)
        return BaseResponseDTO[PlantillaOutDTO](error=False, data=data)

    @router.post("/remplazar", response_model=BaseResponseDTO[str])
    def remplazar(data: CambiarWordDTO):
        codificado = facade.remplazar(data)
        return BaseResponseDTO[str](error=False, data=codificado)

    @router.post(
        "/remplazar_pdf_base64",
        response_model=BaseResponseDTO[str],
        summary="Reemplaza placeholders y devuelve el PDF en base64",
    )
    def remplazar_pdf_base64(data: CambiarWordDTO):
        pdf_b64 = facade.remplazar_y_devolver_pdf(data, devolver_en_base64=True)
        return BaseResponseDTO[str](error=False, data=pdf_b64)

    @router.post(
        "/remplazar_pdf_file",
        summary="Reemplaza placeholders y devuelve el PDF como archivo",
        responses={200: {"content": {"application/pdf": {}}}},
    )
    def remplazar_pdf_file(data: CambiarWordDTO):
        pdf_bytes = facade.remplazar_y_devolver_pdf(data, devolver_en_base64=False)
        out_name = "plantilla.pdf"
        return StreamingResponse(
            content=iter([pdf_bytes]),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{out_name}"',
                "Content-Length": str(len(pdf_bytes)),
            },
        )

    return router
