import json
import logging
from io import StringIO
from shared.logger import get_logger, JSONFormatter


def test_json_output_format():
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JSONFormatter())
    logger = logging.getLogger("test_json")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    logger.info("hello world")
    output = stream.getvalue()
    data = json.loads(output)

    assert data["level"] == "INFO"
    assert data["message"] == "hello world"
    assert "timestamp" in data


def test_get_logger_returns_same_instance():
    a = get_logger("jarvis.test")
    b = get_logger("jarvis.test")
    assert a is b
