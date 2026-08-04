from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):

    APP_NAME: str = "mini-RAG"
    APP_VERSION: str = "0.1.0"
    OPENAI_API_KEY: str ="your_openai_api_key_here"

    FILE_ALLOWED_TYPES: list[str] = ["text/plain", "application/pdf"]
    FILE_MAX_SIZE_MB: int = 10
    FILE_DEFAULT_CHUNK_SIZE: int = 512000

    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "mini-rag"
    
    # ============================== llm config ==============================
    GENERATION_BACKEND_OPTIONS : List[str] = ["OPENAI", "COHERE"]
    EMBEDDING_BACKEND_OPTIONS : List[str] = ["OPENAI", "COHERE", "VOYAGE"]
    GENERATION_BACKEND : str = "openai"
    EMBEDDING_BACKEND : str = "cohere0"

    OPENAI_API_URL : str | None = None 
    COHERE_API_KEY : str | None = None
    VOYAGE_API_KEY : str | None = None

    GENERATION_MODEL_ID : str = "gpt-3.5-turbo-0125"
    EMBEDDING_MODEL_ID : str = "voyage-4-large"
    EMBEDDING_MODEL_SIZE : int | None = None
    
    INPUT_DEFAULT_MAX_CHARACTERS : int = 1024
    GENERATION_DEFAULT_MAX_TOKENS : int = 200
    GENERATION_DEFAULT_TEMPERATURE : float = 0.1
    
    # ============================== Vector db config ==============================
    VECTOR_DB_BACKEND : str = "QDRANT"
    VECTOR_DB_PATH : str = "qdrant_db"
    VECTOR_DB_DISTANCE_METHOD : str | None = None

    model_config = SettingsConfigDict(env_file='.env')

def get_settings():
    return Settings()