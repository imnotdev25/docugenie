
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # FastAPI Settings
    PROJECT_NAME: str = "FastAPI"
    STACK_NAME: str = "fastapi"
    API_PREFIX: str = ""  # api/v1, api versioning

    # Database

    POSTGRES_URI: str = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"

    # RAG
    CHUNK_SIZE: int = 1000

    # Openai
    OPENAI_API_KEY: str = "api-key"
    OPENAI_MODEL: str = "gpt-4o"

settings = Settings()
