from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import logging.config

env_file_path = "/local-envs/.env" if Path("/local-envs/.env").exists() else None

class Settings(BaseSettings):
    entorno: str


    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding="utf-8"
    )

settings = Settings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # para que Uvicorn no se silencie
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] [%(process)d:%(thread)d] [%(filename)s:%(lineno)d]: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "level": "INFO",
        },
        "files_converter_app": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("files_converter_app")