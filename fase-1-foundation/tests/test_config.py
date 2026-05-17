import pytest
from shared.config import get_settings


def test_settings_defaults():
    settings = get_settings()
    assert settings.app_name == "JARVIS-OS"
    assert settings.postgres_port == 5432
    assert settings.redis_port == 6379
    assert settings.embedding_dimensions == 1536


def test_database_url_format():
    settings = get_settings()
    url = settings.database_url
    assert url.startswith("postgresql+asyncpg://")
    assert settings.postgres_db in url


def test_redis_url_format():
    settings = get_settings()
    url = settings.redis_url
    assert url.startswith("redis://")
    assert str(settings.redis_port) in url
