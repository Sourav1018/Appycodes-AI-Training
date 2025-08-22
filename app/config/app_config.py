# app/config/app_config.py
from pydantic import IPvAnyAddress
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    USE_SUPABASE: bool = False
    HOST: IPvAnyAddress
    PORT: int
    RELOAD: bool = False
    OPENAI_API_KEY: str
    QDRANT_API_KEY: str
    QDRANT_CLUSTER_URL: str

    class Config:
        env_file = ".env"  # load from .env automatically


# Create a global settings object
settings = Settings()
