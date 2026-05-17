from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Aplicación
    nombre_app: str = "JARVIS-OS"
    entorno: str = "desarrollo"
    depuracion: bool = False

    # Base de datos
    postgres_usuario: str = "jarvis"
    postgres_contrasena: str = "jarvis_dev"
    postgres_base: str = "jarvis_db"
    postgres_host: str = "localhost"
    postgres_puerto: int = 5432

    @property
    def url_base_datos(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_usuario}:{self.postgres_contrasena}"
            f"@{self.postgres_host}:{self.postgres_puerto}/{self.postgres_base}"
        )

    # Redis
    redis_host: str = "localhost"
    redis_puerto: int = 6379
    redis_db: int = 0

    @property
    def url_redis(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_puerto}/{self.redis_db}"

    # Anthropic
    anthropic_api_key: str = ""
    modelo_claude: str = "claude-sonnet-4-6"
    max_tokens: int = 8192

    # Memoria
    ventana_memoria: int = 20
    modelo_embeddings: str = "text-embedding-3-small"
    dimensiones_embeddings: int = 1536


@lru_cache
def obtener_config() -> Configuracion:
    return Configuracion()
