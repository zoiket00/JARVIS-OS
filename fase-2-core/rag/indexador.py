import re
from pathlib import Path
from rag.embeddings import generar
from rag.buscador import obtener_coleccion


def _limpiar_frontmatter(texto: str) -> str:
    return re.sub(r"^---[\s\S]*?---\n", "", texto).strip()


def _fragmentar(texto: str, max_chars: int = 1000) -> list[str]:
    """Divide el texto en fragmentos por párrafos, máximo max_chars cada uno."""
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    fragmentos, actual = [], ""
    for parrafo in parrafos:
        if len(actual) + len(parrafo) > max_chars and actual:
            fragmentos.append(actual.strip())
            actual = parrafo
        else:
            actual += "\n\n" + parrafo
    if actual.strip():
        fragmentos.append(actual.strip())
    return fragmentos or [texto[:max_chars]]


def indexar_vault(ruta_vault: str, reiniciar: bool = False) -> dict:
    vault = Path(ruta_vault)
    coleccion = obtener_coleccion()

    if reiniciar:
        ids_existentes = coleccion.get()["ids"]
        if ids_existentes:
            coleccion.delete(ids=ids_existentes)

    notas = [p for p in vault.rglob("*.md") if not any(part.startswith(".") for part in p.parts)]

    ids, documentos, metadatos = [], [], []
    for nota in notas:
        try:
            texto = nota.read_text(encoding="utf-8")
            contenido = _limpiar_frontmatter(texto)
            if len(contenido) < 50:
                continue
            ruta_rel = str(nota.relative_to(vault))
            titulo = nota.stem.replace("-", " ").replace("_", " ")
            for i, fragmento in enumerate(_fragmentar(contenido)):
                doc_id = f"{ruta_rel}::{i}"
                if doc_id not in (coleccion.get(ids=[doc_id])["ids"] or []):
                    ids.append(doc_id)
                    documentos.append(fragmento)
                    metadatos.append({"ruta": ruta_rel, "titulo": titulo})
        except Exception:
            continue

    if ids:
        embeddings = generar(documentos)
        coleccion.add(ids=ids, documents=documentos, embeddings=embeddings, metadatas=metadatos)

    return {"indexadas": len(notas), "fragmentos_nuevos": len(ids), "total": coleccion.count()}
