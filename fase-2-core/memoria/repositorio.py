import aiosqlite
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent.parent / "jarvis_memoria.db"


async def _init_db(conn: aiosqlite.Connection) -> None:
    await conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sesion_id TEXT NOT NULL,
            rol TEXT NOT NULL,
            contenido TEXT NOT NULL,
            creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS nodos_conocimiento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            etiquetas TEXT DEFAULT '[]',
            fuente TEXT DEFAULT '',
            actualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_conversaciones_sesion
            ON conversaciones (sesion_id, creado_en DESC);
    """)
    await conn.commit()


async def obtener_pool() -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await _init_db(conn)


async def cerrar_pool() -> None:
    pass


async def guardar_mensaje(sesion_id: str, rol: str, contenido: str, metadatos: dict[str, Any] | None = None) -> str:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "INSERT INTO conversaciones (sesion_id, rol, contenido) VALUES (?, ?, ?)",
            (sesion_id, rol, contenido),
        )
        await conn.commit()
        return str(cursor.lastrowid)


async def obtener_historial(sesion_id: str, limite: int = 20) -> list[dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute(
            "SELECT rol, contenido FROM conversaciones WHERE sesion_id = ? ORDER BY creado_en DESC LIMIT ?",
            (sesion_id, limite),
        ) as cur:
            filas = await cur.fetchall()
    return [{"rol": f["rol"], "contenido": f["contenido"]} for f in reversed(filas)]


async def guardar_conocimiento(titulo: str, contenido: str, etiquetas: list[str] | None = None, fuente: str = "") -> str:
    import json
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "INSERT INTO nodos_conocimiento (titulo, contenido, etiquetas, fuente) VALUES (?, ?, ?, ?)",
            (titulo, contenido, json.dumps(etiquetas or []), fuente),
        )
        await conn.commit()
        return str(cursor.lastrowid)


async def buscar_conocimiento(consulta: str, limite: int = 5) -> list[dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute(
            "SELECT titulo, contenido, etiquetas, fuente FROM nodos_conocimiento WHERE contenido LIKE ? OR titulo LIKE ? ORDER BY actualizado_en DESC LIMIT ?",
            (f"%{consulta}%", f"%{consulta}%", limite),
        ) as cur:
            filas = await cur.fetchall()
    return [{"titulo": f["titulo"], "contenido": f["contenido"], "etiquetas": f["etiquetas"], "fuente": f["fuente"]} for f in filas]
