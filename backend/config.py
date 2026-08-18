from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    COGNO_URI: str = "bolt://localhost:7687"
    COGNO_USER: str = "neo4j"
    COGNO_PASSWORD: str = "password"
    DATABASE_NAME: str = "neo4j"
    
    MAX_CONNECTION_POOL_SIZE: int = 50
    CONNECTION_TIMEOUT_SECONDS: float = 5.0
    
    APP_NAME: str = "GraphGuard - Supply Chain Risk & Cascading Failure Simulator"
    APP_ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    ENABLE_DEMO_FALLBACK: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
