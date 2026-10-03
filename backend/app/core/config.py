import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    WATSONX_API_KEY: str | None = os.getenv("WATSONX_API_KEY")
    WATSONX_PROJECT_ID: str | None = os.getenv("WATSONX_PROJECT_ID")
    WATSONX_URL: str | None = os.getenv("WATSONX_URL")
    WATSONX_MODEL_ID: str | None = os.getenv("WATSONX_MODEL_ID")
    
    WATSONX_ASSISTANT_ID: str | None = os.getenv("WATSONX_ASSISTANT_ID")
    WATSONX_ASSISTANT_URL: str | None = os.getenv("WATSONX_ASSISTANT_URL")
    
    WATSONX_ORCHESTRATE_URL: str | None = os.getenv("WATSONX_ORCHESTRATE_URL")
    WATSONX_ORCHESTRATE_API_KEY: str | None = os.getenv("WATSONX_ORCHESTRATE_API_KEY")
    
    VECTOR_STORE_PATH: str = os.getenv("VECTOR_STORE_PATH", "./data/vector_store")
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "local")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "local")

    class Config:
        env_file = ".env"

settings = Settings()
