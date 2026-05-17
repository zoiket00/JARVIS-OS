import asyncpg
from typing import Any
from config import obtener_config

_pool: asyncpg.Pool | None = None


async def obtener_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        cfg = obtener_config()
        _pool = await asyncpg.create_pool(cfg.url_base_datos, min_size=2, max_size=10)
    return _pool


async def cerrar_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


async def guardar_mensaje(sesion_id: str, rol: str, contenido: str, metadatos: dict[str, Any] | None = None) -> str:
    pool = await obtener_pool()
    async with pool.acquire() as conn:
        fila = await conn.fetchrow(
            """
            INSERT INTO conversaciones (sesion_id, rol, contenido, metadatos)
            VALUES ($1, $2, $3, $4::jsonb)
            RETURNING id::text
            """,
            sesion_id, rol, contenido, str(metadatos or {}).replace("'", '"'),
        )
    return fila["id"]


async def obtener_historial(sesion_id: str, limite: int = 20) -> list[dict[str, Any]]:
    pool = await obtener_pool()
    async with pool.acquire() as conn:
        filas = await conn.fetch(
            """
            SELECT rol, contenido, creado_en
            FROM conversaciones
            WHERE sesion_id = $1
            ORDER BY creado_en DESC
            LIMIT $2
            """,
            sesion_id, limite,
        )
    return [{"rol": f["rol"], "contenido": f["contenido"]} for f in reversed(filas)]


async def guardar_conocimiento(titulo: str, contenido: str, etiquetas: list[str] | None = None, fuente: str = "") -> str:
    pool = await obtener_pool()
    async with pool.acquire() as conn:
        fila = await conn.fetchrow(
            """
            INSERT INTO nodos_conocimiento (titulo, contenido, etiquetas, fuente)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT DO NOTHING
            RETURNING id::text
            """,
            titulo, contenido, etiquetas or [], fuente,
        )
    return fila["id"] if fila else "duplicado"


async def buscar_conocimiento(consulta: str, limite: int = 5) -> list[dict[str, Any]]:
    pool = await obtener_pool()
    async with pool.acquire() as conn:
        filas = await conn.fetch(
            """
            SELECT titulo, contenido, etiquetas, fuente
            FROM nodos_conocimiento
            WHERE contenido ILIKE $1 OR titulo ILIKE $1
            ORDER BY actualizado_en DESC
            LIMIT $2
            """,
            f"%{consulta}%", limite,
        )
    return [dict(f) for f in filas]
