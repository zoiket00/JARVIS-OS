from rag.buscador import buscar, total_notas_indexadas

HERRAMIENTAS = [
    {
        "type": "function",
        "function": {
            "name": "buscar_vault_semantico",
            "description": "Búsqueda semántica sobre las notas del vault de Obsidian. Encuentra notas relevantes aunque no contengan las palabras exactas. Úsalo cuando el usuario pregunte sobre conceptos, ideas o conocimiento que podría estar en el vault.",
            "parameters": {
                "type": "object",
                "properties": {
                    "consulta": {"type": "string", "description": "Pregunta o concepto a buscar semánticamente"},
                    "n_resultados": {"type": "integer", "description": "Número de notas a retornar (default: 3)", "default": 3},
                },
                "required": ["consulta"],
            },
        },
    },
]


async def ejecutar(nombre: str, parametros: dict) -> str:
    if nombre == "buscar_vault_semantico":
        total = total_notas_indexadas()
        if total == 0:
            return "El vault no está indexado aún. Llama al endpoint POST /rag/indexar primero."

        resultados = buscar(parametros["consulta"], n_resultados=parametros.get("n_resultados", 3))
        if not resultados:
            return "No encontré notas relevantes en el vault."

        salida = f"Encontré {len(resultados)} notas relevantes:\n\n"
        for r in resultados:
            salida += f"### {r['titulo']} — similitud: {r['similitud']}\n{r['contenido'][:300]}\n\n"
        return salida

    return f"Herramienta desconocida: {nombre}"
