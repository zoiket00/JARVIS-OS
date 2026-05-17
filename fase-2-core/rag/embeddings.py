from functools import lru_cache
from sentence_transformers import SentenceTransformer

MODELO = "all-MiniLM-L6-v2"  # 384 dims, ~90MB, corre en CPU


@lru_cache(maxsize=1)
def obtener_modelo() -> SentenceTransformer:
    return SentenceTransformer(MODELO)


def generar(textos: list[str]) -> list[list[float]]:
    modelo = obtener_modelo()
    return modelo.encode(textos, convert_to_numpy=True).tolist()


def generar_uno(texto: str) -> list[float]:
    return generar([texto])[0]
