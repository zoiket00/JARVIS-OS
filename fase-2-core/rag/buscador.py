from functools import lru_cache
from pathlib import Path
import chromadb
from rag.embeddings import generar_uno

DB_PATH = Path(__file__).parent.parent / "jarvis_vectores"
COLECCION = "vault_obsidian"


@lru_cache(maxsize=1)
def obtener_coleccion() -> chromadb.Collection:
    cliente = chromadb.PersistentClient(path=str(DB_PATH))
    return cliente.get_or_create_collection(
        name=COLECCION,
        metadata={"hnsw:space": "cosine"},
    )


def buscar(consulta: str, n_resultados: int = 5) -> list[dict]:
    coleccion = obtener_coleccion()
    if coleccion.count() == 0:
        return []

    embedding = generar_uno(consulta)
    resultados = coleccion.query(
        query_embeddings=[embedding],
        n_results=min(n_resultados, coleccion.count()),
        include=["documents", "metadatas", "distances"],
    )

    notas = []
    for i, doc in enumerate(resultados["documents"][0]):
        notas.append({
            "contenido": doc,
            "ruta": resultados["metadatas"][0][i].get("ruta", ""),
            "titulo": resultados["metadatas"][0][i].get("titulo", ""),
            "similitud": round(1 - resultados["distances"][0][i], 3),
        })
    return notas


def total_notas_indexadas() -> int:
    return obtener_coleccion().count()
