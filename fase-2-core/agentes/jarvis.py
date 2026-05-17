import anthropic
from config import obtener_config
from memoria.repositorio import guardar_mensaje, obtener_historial
from agentes.herramientas import TODAS, ejecutar

SISTEMA = """Eres JARVIS — sistema personal de inteligencia aumentada.

No eres un chatbot. Eres un sistema que razona, recuerda y actúa.

Reglas:
- Responde siempre en español
- Cuando el usuario quiera que recuerdes algo, usa guardar_en_memoria
- Cuando necesites información guardada, usa buscar_en_memoria
- Cuando necesites consultar el vault de Obsidian, usa leer_nota_vault o listar_vault
- Sé preciso y directo — no hay rodeos innecesarios
"""


async def procesar(sesion_id: str, mensaje_usuario: str) -> str:
    cfg = obtener_config()
    cliente = anthropic.AsyncAnthropic(api_key=cfg.anthropic_api_key)

    # Cargar historial de la sesión
    historial = await obtener_historial(sesion_id, limite=cfg.max_tokens // 200)

    # Construir mensajes para Claude
    mensajes = [
        {"role": "user" if m["rol"] == "usuario" else "assistant", "content": m["contenido"]}
        for m in historial
    ]
    mensajes.append({"role": "user", "content": mensaje_usuario})

    # Guardar mensaje del usuario
    await guardar_mensaje(sesion_id, "usuario", mensaje_usuario)

    # Bucle de razonamiento con tool use
    respuesta_final = ""
    while True:
        respuesta = await cliente.messages.create(
            model=cfg.modelo_claude,
            max_tokens=cfg.max_tokens,
            system=SISTEMA,
            tools=TODAS,
            messages=mensajes,
        )

        # Procesar bloques de respuesta
        for bloque in respuesta.content:
            if bloque.type == "text":
                respuesta_final = bloque.text

        # Si Claude quiere usar herramientas
        if respuesta.stop_reason == "tool_use":
            resultados_herramientas = []

            for bloque in respuesta.content:
                if bloque.type == "tool_use":
                    resultado = await ejecutar(bloque.name, bloque.input)
                    resultados_herramientas.append({
                        "type": "tool_result",
                        "tool_use_id": bloque.id,
                        "content": resultado,
                    })

            # Añadir respuesta de Claude y resultados al historial
            mensajes.append({"role": "assistant", "content": respuesta.content})
            mensajes.append({"role": "user", "content": resultados_herramientas})
            continue

        # Sin más herramientas — respuesta final
        break

    await guardar_mensaje(sesion_id, "asistente", respuesta_final)
    return respuesta_final
