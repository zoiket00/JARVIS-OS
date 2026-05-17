from . import memoria, vault, vault_rag

TODAS = memoria.HERRAMIENTAS + vault.HERRAMIENTAS + vault_rag.HERRAMIENTAS

_nombres_memoria = {h["function"]["name"] for h in memoria.HERRAMIENTAS}
_nombres_vault = {h["function"]["name"] for h in vault.HERRAMIENTAS}
_nombres_rag = {h["function"]["name"] for h in vault_rag.HERRAMIENTAS}


async def ejecutar(nombre: str, parametros: dict) -> str:
    if nombre in _nombres_memoria:
        return await memoria.ejecutar(nombre, parametros)
    if nombre in _nombres_vault:
        return await vault.ejecutar(nombre, parametros)
    if nombre in _nombres_rag:
        return await vault_rag.ejecutar(nombre, parametros)
    return f"Herramienta no registrada: {nombre}"
