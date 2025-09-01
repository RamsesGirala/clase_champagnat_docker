from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from exceptions.tributarios_exception import TributarioException
from facades.files_converter_facade import FilesConverterFacade
from presentation.handler import global_exception_handler,tributario_exception_handler
from presentation.files_converter_controller import get_files_converter_router
from services.word_to_pdf_converter_service import WordToPdfConverterService
from settings.config import settings,logger
from services.health_service import HealthService
from presentation.health_controller import get_health_router
import logging

logger.info(f"Iniciando aplicación de files converter con configuracion: {settings}")

# Instanciar las dependencias
word_to_pdf_service = WordToPdfConverterService()
files_converter_facade = FilesConverterFacade(word_to_pdf_service=word_to_pdf_service)
health_service = HealthService()


app = FastAPI(docs_url="/archivos/docs",openapi_url="/archivos/openapi.json")

app.include_router(get_files_converter_router(files_converter_facade), prefix="/archivos/api", tags=["Archivos"])
app.include_router(get_health_router(health_service))
app.add_exception_handler(TributarioException,tributario_exception_handler)
app.add_exception_handler(Exception,global_exception_handler)

class HealthEndpointFilter(logging.Filter):
    def filter(self, record):
        # El mensaje del log contiene la ruta, como: "GET /health/liveness HTTP/1.1"
        return not (
            "GET /health" in record.getMessage()
            or "POST /health" in record.getMessage()
        )

# Agregar el filtro al logger de access logs de uvicorn
uvicorn_access_logger = logging.getLogger("uvicorn.access")
uvicorn_access_logger.addFilter(HealthEndpointFilter())

#Habilitar CORS
origins = [
    "http://localhost:3000",  # tu frontend local
    "https://miapp-frontend.com",  # si tenés prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # también podés usar ["*"] para todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
