import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Production RAG Bot"
    
    GOOGLE_API_KEY: str
    OPENROUTER_API_KEY: str 
    
    CHROMA_DB_DIR: str = "chroma_db_data"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()