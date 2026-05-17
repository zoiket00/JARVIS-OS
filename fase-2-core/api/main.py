from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uuid

from agentes.jarvis import procesar
from memoria.repositorio import obtener_pool, cerrar_pool
from config import obtener_config


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    await obtener_pool()
    yield
    await cerrar_pool()


app = FastAPI(
    title="JARVIS-OS API",
    description="Sistema operativo de IA personal — razona, recuerda y actúa",
    version="0.3.0",
    lifespan=ciclo_de_vida,
)


class SolicitudChat(BaseModel):
    mensaje: str
    sesion_id: str | None = None


class RespuestaChat(BaseModel):
    respuesta: str
    sesion_id: str


@app.get("/salud")
async def salud():
    from rag.buscador import total_notas_indexadas
    return {
        "estado": "ok",
        "servicio": "JARVIS-OS",
        "notas_indexadas": total_notas_indexadas(),
    }


@app.post("/chat", response_model=RespuestaChat)
async def chat(solicitud: SolicitudChat):
    sesion_id = solicitud.sesion_id or str(uuid.uuid4())
    try:
        respuesta = await procesar(sesion_id, solicitud.mensaje)
        return RespuestaChat(respuesta=respuesta, sesion_id=sesion_id)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sesion/{sesion_id}/historial")
async def historial(sesion_id: str, limite: int = 20):
    from memoria.repositorio import obtener_historial
    mensajes = await obtener_historial(sesion_id, limite)
    return {"sesion_id": sesion_id, "mensajes": mensajes}


@app.post("/rag/indexar")
async def indexar(background_tasks: BackgroundTasks, reiniciar: bool = False):
    from rag.indexador import indexar_vault
    cfg = obtener_config()

    def _tarea():
        resultado = indexar_vault(cfg.vault_ruta, reiniciar=reiniciar)
        print(f"[RAG] Indexación completa: {resultado}")

    background_tasks.add_task(_tarea)
    return {"estado": "indexando", "vault": cfg.vault_ruta, "reiniciar": reiniciar}


@app.get("/rag/estado")
async def estado_rag():
    from rag.buscador import total_notas_indexadas
    return {"notas_indexadas": total_notas_indexadas()}
