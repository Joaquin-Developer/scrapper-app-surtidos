import os
from typing import Dict
from dataclasses import dataclass


@dataclass
class Config:
    DEBUG = True
    API_URL = "http://localhost:8081"
    API_USERNAME = ""
    API_PASSWORD = ""


@dataclass
class ProductionConfig(Config):
    DEBUG = False
    API_URL = None
    API_USERNAME = os.getenv("API_USERNAME")
    API_PASSWORD = os.getenv("API_PASSWORD")


ENV = os.getenv("environment") or "development"

_config : Dict[str, Config] = {
    "development": Config,
    "production": ProductionConfig,
}

config = _config[ENV]
