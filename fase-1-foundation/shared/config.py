from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "JARVIS-OS"
    app_env: str = "development"
    debug: bool = False

    # Database
    postgres_user: str = "jarvis"
    postgres_password: str = "jarvis_dev"
    postgres_db: str = "jarvis_db"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # Anthropic
    anthropic_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"
    claude_max_tokens: int = 8192

    # Memory
    memory_window: int = 20
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536


@lru_cache
def get_settings() -> Settings:
    return Settings()
