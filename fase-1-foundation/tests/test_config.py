import pytest
from shared.config import obtener_config


def test_valores_por_defecto():
    config = obtener_config()
    assert config.nombre_app == "JARVIS-OS"
    assert config.postgres_puerto == 5432
    assert config.redis_puerto == 6379
    assert config.dimensiones_embeddings == 1536


def test_formato_url_base_datos():
    config = obtener_config()
    url = config.url_base_datos
    assert url.startswith("postgresql+asyncpg://")
    assert config.postgres_base in url


def test_formato_url_redis():
    config = obtener_config()
    url = config.url_redis
    assert url.startswith("redis://")
    assert str(config.redis_puerto) in url
