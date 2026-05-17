import json
from openai import AsyncOpenAI, BadRequestError, RateLimitError
from config import obtener_config
from memoria.repositorio import guardar_mensaje, obtener_historial
from agentes.herramientas import TODAS, ejecutar

SISTEMA = """Eres JARVIS — sistema personal de inteligencia aumentada.

No eres un chatbot. Eres un sistema que razona, recuerda y actúa.

Reglas:
- Responde siempre en español
- Cuando el usuario quiera que recuerdes algo, usa guardar_en_memoria
- Cuando necesites recuperar algo guardado, usa buscar_en_memoria
- Cuando el usuario pregunte por conocimiento del vault, usa buscar_vault_semantico
- Cuando necesites leer una nota específica, usa leer_nota_vault
- Sé preciso y directo — sin rodeos innecesarios
"""


def _cliente_groq() -> AsyncOpenAI:
    cfg = obtener_config()
    return AsyncOpenAI(
        api_key=cfg.groq_api_key,
        base_url="https://api.groq.com/openai/v1",
    )


async def procesar(sesion_id: str, mensaje_usuario: str) -> str:
    cfg = obtener_config()
    cliente = _cliente_groq()

    historial = await obtener_historial(sesion_id, limite=10)
    mensajes = [
        {"role": "user" if m["rol"] == "usuario" else "assistant", "content": m["contenido"]}
        for m in historial
    ]
    mensajes.append({"role": "user", "content": mensaje_usuario})
    await guardar_mensaje(sesion_id, "usuario", mensaje_usuario)

    respuesta_final = ""
    intentos = 0

    while intentos < 5:
        intentos += 1
        try:
            respuesta = await cliente.chat.completions.create(
                model=cfg.modelo,
                max_tokens=min(cfg.max_tokens, 4096),
                messages=[{"role": "system", "content": SISTEMA}] + mensajes,
                tools=TODAS,
                tool_choice="auto",
            )
        except RateLimitError:
            respuesta_final = "Límite de tokens de Groq alcanzado. Intenta de nuevo en unos minutos."
            break
        except BadRequestError:
            # Fallo en tool use — reintentar sin herramientas
            try:
                respuesta = await cliente.chat.completions.create(
                    model=cfg.modelo,
                    max_tokens=min(cfg.max_tokens, 4096),
                    messages=[{"role": "system", "content": SISTEMA}] + mensajes,
                )
                respuesta_final = respuesta.choices[0].message.content or ""
            except Exception:
                respuesta_final = "No pude procesar la solicitud. Intenta reformularla."
            break

        mensaje_asistente = respuesta.choices[0].message

        if mensaje_asistente.content:
            respuesta_final = mensaje_asistente.content

        if not mensaje_asistente.tool_calls:
            break

        mensajes.append(mensaje_asistente)
        for llamada in mensaje_asistente.tool_calls:
            try:
                parametros = json.loads(llamada.function.arguments or "{}") or {}
                resultado = await ejecutar(llamada.function.name, parametros)
            except Exception as e:
                resultado = f"Error ejecutando {llamada.function.name}: {e}"
            mensajes.append({
                "role": "tool",
                "tool_call_id": llamada.id,
                "content": resultado,
            })

    await guardar_mensaje(sesion_id, "asistente", respuesta_final)
    return respuesta_final
