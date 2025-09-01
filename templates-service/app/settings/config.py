from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import logging.config

env_file_path = "/local-envs/.env" if Path("/local-envs/.env").exists() else None

class Settings(BaseSettings):
    entorno: str
    mongo_url: str
    file_converter_base_url: str

    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding="utf-8"
    )

    @property
    def jwt_issuers_list(self) -> list[str]:
        return [i.strip() for i in self.jwt_issuers.split(",")]

    @property
    def jwt_jwks_list(self) -> list[str]:
        return [j.strip() for j in self.jwt_jwks.split(",")]

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
        "apscheduler": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False
        },
        "templates_app": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False
        }
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("templates_app")