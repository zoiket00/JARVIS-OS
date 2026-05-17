from . import memoria, vault

# Todas las herramientas disponibles para Claude
TODAS = memoria.HERRAMIENTAS + vault.HERRAMIENTAS


async def ejecutar(nombre: str, parametros: dict) -> str:
    if nombre in {h["name"] for h in memoria.HERRAMIENTAS}:
        return await memoria.ejecutar(nombre, parametros)
    if nombre in {h["name"] for h in vault.HERRAMIENTAS}:
        return await vault.ejecutar(nombre, parametros)
    return f"Herramienta no registrada: {nombre}"
