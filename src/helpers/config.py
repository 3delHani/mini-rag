from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str = "mini-RAG"
    APP_VERSION: str = "0.1.0"
    OPENAI_API_KEY: str ="your_openai_api_key_here"

    FILE_ALLOWED_TYPES: list[str] = ["text/plain", "application/pdf"]
    FILE_MAX_SIZE_MB: int = 10
    FILE_DEFAULT_CHUNK_SIZE: int = 512000

    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "mini-rag"

    model_config = SettingsConfigDict(env_file='.env')

def get_settings():
    return Settings()