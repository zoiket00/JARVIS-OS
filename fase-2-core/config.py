from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    entorno: str = "desarrollo"
    depuracion: bool = False

    postgres_usuario: str = "jarvis"
    postgres_contrasena: str = "jarvis_dev"
    postgres_base: str = "jarvis_db"
    postgres_host: str = "localhost"
    postgres_puerto: int = 5432

    @property
    def url_base_datos(self) -> str:
        return (
            f"postgresql://{self.postgres_usuario}:{self.postgres_contrasena}"
            f"@{self.postgres_host}:{self.postgres_puerto}/{self.postgres_base}"
        )

    redis_host: str = "localhost"
    redis_puerto: int = 6379
    redis_db: int = 0

    anthropic_api_key: str = ""
    modelo_claude: str = "claude-sonnet-4-6"
    max_tokens: int = 8192

    vault_ruta: str = r"c:\Claude - Obsidian\Dios de la IA"


@lru_cache
def obtener_config() -> Configuracion:
    return Configuracion()
