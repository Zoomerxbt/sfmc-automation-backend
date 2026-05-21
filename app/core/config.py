import os
from pathlib import Path
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Calculate absolute path to your project root directory dynamically
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = os.path.join(ROOT_DIR, ".env")


class Settings(BaseSettings):
    """
    Application settings class using Pydantic BaseSettings.
    Mapped directly to your specific .env variables.
    """
    PROJECT_NAME: str = "SFMC Automation API"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"

    # Core Secrets (Matching your exact environment variables)
    API_KEY: str = Field(...)
    CLIENT_ID: str = Field(...)
    AUTH_BASE_URI: str = Field(...)
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: Union[List[str], str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if not v:
            return []
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return []

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8", 
        extra="ignore"
        
    )

settings = Settings()  # type: ignore