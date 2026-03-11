from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    App_Name: str
    App_Version: str
    OPENAI_API_KEY: str
    
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE_MB: int
    FILE_DEFAULT_CHUNK_SIZE:  int
    
    MONGODB_URL: str
    MONGODB_DB_DATEBASE: str
    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()