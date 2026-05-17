import os
from pathlib import Path
from config import obtener_config

HERRAMIENTAS = [
    {
        "name": "leer_nota_vault",
        "description": "Lee el contenido de una nota del vault de Obsidian (base de conocimiento de JARVIS). Úsalo para consultar información almacenada en el vault.",
        "input_schema": {
            "type": "object",
            "properties": {
                "ruta": {"type": "string", "description": "Ruta relativa de la nota dentro del vault (ej: 'wiki/concepts/transformers.md')"},
            },
            "required": ["ruta"],
        },
    },
    {
        "name": "listar_vault",
        "description": "Lista las notas disponibles en una carpeta del vault de Obsidian.",
        "input_schema": {
            "type": "object",
            "properties": {
                "carpeta": {"type": "string", "description": "Carpeta a listar (ej: 'wiki/concepts'). Vacío para la raíz.", "default": ""},
            },
            "required": [],
        },
    },
]


async def ejecutar(nombre: str, parametros: dict) -> str:
    cfg = obtener_config()
    vault = Path(cfg.vault_ruta)

    if nombre == "leer_nota_vault":
        ruta_nota = vault / parametros["ruta"]
        if not ruta_nota.exists():
            return f"Nota no encontrada: {parametros['ruta']}"
        if not ruta_nota.is_relative_to(vault):
            return "Acceso denegado: ruta fuera del vault."
        return ruta_nota.read_text(encoding="utf-8")

    if nombre == "listar_vault":
        carpeta = parametros.get("carpeta", "")
        directorio = vault / carpeta if carpeta else vault
        if not directorio.exists():
            return f"Carpeta no encontrada: {carpeta}"
        notas = [
            str(p.relative_to(vault))
            for p in directorio.rglob("*.md")
            if not any(part.startswith(".") for part in p.parts)
        ]
        return "\n".join(sorted(notas)) if notas else "Sin notas en esta carpeta."

    return f"Herramienta desconocida: {nombre}"
