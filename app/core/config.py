from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Home Designer"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "default_secret_key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520 # 8 days
    
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ai_home_designer"
    
    OPENAI_API_KEY: str = ""
    
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
