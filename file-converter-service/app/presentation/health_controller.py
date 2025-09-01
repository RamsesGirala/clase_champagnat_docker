from fastapi import APIRouter, Response, status
from services.health_service import HealthService

def get_health_router(health_service: HealthService) -> APIRouter:
    router = APIRouter()

    @router.get("/health/liveness", tags=["Health"])
    def liveness_check():
        return {"status": "ok"}

    @router.get("/health/readiness", tags=["Health"])
    def readiness_check():
        if health_service.is_ready():
            return {"status": "ready"}
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)

    return router
