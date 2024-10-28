# app/core/config.py
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv() 

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "PDF Extractor Backend")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    PORT: int = int(os.getenv("PORT", 8000))

# Instancia de la configuración
settings = Settings()
