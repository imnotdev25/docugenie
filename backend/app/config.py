
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # FastAPI Settings
    PROJECT_NAME: str = "FastAPI"
    STACK_NAME: str = "fastapi-rag-azure"
    API_PREFIX: str = ""  # api/v1, api versioning

    # Database
    POSTGRES_URI: str = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"

    # RAG
    CHUNK_SIZE: int = 1536
    DEFAULT_SEARCH_LIMIT: int = 5

    # S3
    S3_BUCKET: str = "bucket-name"
    S3_REGION: str = "us-west-2"
    S3_KEY_ID: str = "access-key"
    S3_SECRET_KEY: str = "secret-key"

    # Openai
    OPENAI_API_KEY: str = "api-key"
    OPENAI_MODEL: str = "gpt-4o"

    # Azure AI
    AZURE_ENDPOINT: str = "https://api.openai.com"
    AZURE_API_KEY: str = "api-key"
    AZURE_API_VERSION: str = "2021-09-01"

    # Logging
    LOGFIRE_TOKEN: str = "logfire-token"
    LOGFIRE_PROJECT: str = "logfire-project"

    # Uploads
    UPLOAD_DIR: str = "uploads"


settings = Settings()
