import json
import logging
from io import StringIO
from shared.logger import obtener_logger, FormateadorJSON


def test_formato_salida_json():
    flujo = StringIO()
    manejador = logging.StreamHandler(flujo)
    manejador.setFormatter(FormateadorJSON())
    logger = logging.getLogger("prueba_json")
    logger.addHandler(manejador)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    logger.info("hola mundo")
    salida = flujo.getvalue()
    datos = json.loads(salida)

    assert datos["nivel"] == "INFO"
    assert datos["mensaje"] == "hola mundo"
    assert "timestamp" in datos


def test_misma_instancia_logger():
    a = obtener_logger("jarvis.prueba")
    b = obtener_logger("jarvis.prueba")
    assert a is b
