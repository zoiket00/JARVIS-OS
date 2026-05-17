from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

from agentes.jarvis import procesar
from memoria.repositorio import obtener_pool, cerrar_pool


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    await obtener_pool()
    yield
    await cerrar_pool()


app = FastAPI(
    title="JARVIS-OS API",
    description="Sistema operativo de IA personal — razona, recuerda y actúa",
    version="0.2.0",
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
    return {"estado": "ok", "servicio": "JARVIS-OS"}


@app.post("/chat", response_model=RespuestaChat)
async def chat(solicitud: SolicitudChat):
    sesion_id = solicitud.sesion_id or str(uuid.uuid4())
    try:
        respuesta = await procesar(sesion_id, solicitud.mensaje)
        return RespuestaChat(respuesta=respuesta, sesion_id=sesion_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sesion/{sesion_id}/historial")
async def historial(sesion_id: str, limite: int = 20):
    from memoria.repositorio import obtener_historial
    mensajes = await obtener_historial(sesion_id, limite)
    return {"sesion_id": sesion_id, "mensajes": mensajes}
