from memoria.repositorio import guardar_conocimiento, buscar_conocimiento

HERRAMIENTAS = [
    {
        "type": "function",
        "function": {
            "name": "guardar_en_memoria",
            "description": "Guarda un hecho, nota o conocimiento importante en la base de datos persistente de JARVIS. Úsalo cuando el usuario quiera que recuerdes algo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "description": "Título breve del conocimiento"},
                    "contenido": {"type": "string", "description": "Contenido completo a guardar"},
                    "etiquetas": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Etiquetas para categorizar (ej: ['python', 'arquitectura'])"
                    },
                },
                "required": ["titulo", "contenido"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_en_memoria",
            "description": "Busca en la memoria persistente de JARVIS usando palabras clave.",
            "parameters": {
                "type": "object",
                "properties": {
                    "consulta": {"type": "string", "description": "Términos de búsqueda"},
                    "limite": {"type": "integer", "description": "Máximo de resultados (default: 5)"},
                },
                "required": ["consulta"],
            },
        },
    },
]


async def ejecutar(nombre: str, parametros: dict) -> str:
    if nombre == "guardar_en_memoria":
        id_nodo = await guardar_conocimiento(
            titulo=parametros["titulo"],
            contenido=parametros["contenido"],
            etiquetas=parametros.get("etiquetas", []),
        )
        return f"Guardado con ID: {id_nodo}"

    if nombre == "buscar_en_memoria":
        resultados = await buscar_conocimiento(
            consulta=parametros["consulta"],
            limite=parametros.get("limite", 5),
        )
        if not resultados:
            return "No encontré nada relacionado en la memoria."
        return "\n\n".join(f"**{r['titulo']}**\n{r['contenido']}" for r in resultados)

    return f"Herramienta desconocida: {nombre}"
