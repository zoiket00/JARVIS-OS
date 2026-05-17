import logging
import sys
from typing import Any
import json
from datetime import datetime, timezone


class FormateadorJSON(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        entrada: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "nivel": record.levelname,
            "logger": record.name,
            "mensaje": record.getMessage(),
        }
        if record.exc_info:
            entrada["excepcion"] = self.formatException(record.exc_info)
        if hasattr(record, "extra"):
            entrada.update(record.extra)
        return json.dumps(entrada, ensure_ascii=False)


def obtener_logger(nombre: str) -> logging.Logger:
    logger = logging.getLogger(nombre)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    manejador = logging.StreamHandler(sys.stdout)
    manejador.setFormatter(FormateadorJSON())
    logger.addHandler(manejador)
    logger.propagate = False
    return logger
