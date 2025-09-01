from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from exceptions.tributarios_exception import TributarioException
from facades.plantillas_facade import PlantillasFacade
from presentation.handler import global_exception_handler,tributario_exception_handler
from presentation.plantillas_controller import get_plantillas_router
from repositories.plantillas_repository import PlantillasRepository
from services.files_converter_client import FileConverterClient
from services.files_service import FileService
from services.plantillas_service import PlantillasService
from services.word_replacer_service import WordReplacerService
from settings.config import settings,logger
from services.health_service import HealthService
from presentation.health_controller import get_health_router
import logging


logger.info(f"Iniciando aplicación de plantillas con configuracion: {settings}")

# Conectar a MongoDB usando la URL de configuración
mongo_client = MongoClient(settings.mongo_url)
db = mongo_client.get_default_database()
plantillas_collection = db["plantillas"]

# Instanciar las dependencias
plantillas_repository = PlantillasRepository(plantillas_collection)
plantillas_service = PlantillasService(plantillas_repository)

files_service = FileService()
replacer_service = WordReplacerService()
files_client = FileConverterClient()
plantillas_facade = PlantillasFacade(plantillas_service=plantillas_service,files_service=files_service,
                                     replacer_service=replacer_service, files_converter_client=files_client)
health_service = HealthService(db)



app = FastAPI(docs_url="/plantillas/docs",openapi_url="/plantillas/openapi.json")

app.include_router(get_plantillas_router(plantillas_facade), prefix="/plantillas/api", tags=["Plantillas"])
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
