import pytest
from agentes.herramientas import TODAS, ejecutar
from agentes.herramientas import vault


def test_herramientas_registradas():
    nombres = {h["name"] for h in TODAS}
    assert "guardar_en_memoria" in nombres
    assert "buscar_en_memoria" in nombres
    assert "leer_nota_vault" in nombres
    assert "listar_vault" in nombres


def test_cada_herramienta_tiene_descripcion():
    for herramienta in TODAS:
        assert herramienta.get("description"), f"{herramienta['name']} sin descripción"
        assert herramienta.get("input_schema"), f"{herramienta['name']} sin esquema"


@pytest.mark.asyncio
async def test_vault_nota_inexistente():
    resultado = await vault.ejecutar("leer_nota_vault", {"ruta": "no-existe.md"})
    assert "no encontrada" in resultado.lower()


@pytest.mark.asyncio
async def test_herramienta_desconocida():
    resultado = await ejecutar("herramienta_fantasma", {})
    assert "no registrada" in resultado.lower()
