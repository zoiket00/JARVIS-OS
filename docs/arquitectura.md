# JARVIS-OS — Arquitectura de 3 Capas

> El sistema no responde preguntas — toma decisiones, ejecuta acciones y genera resultados.

---

## Las 3 Capas

```
┌─────────────────────────────────────────────────────┐
│           🧠  CAPA 1 — CONOCIMIENTO                 │
│                    Obsidian                          │
│        Notas Markdown · Fuente de verdad             │
│        Contexto histórico · Decisiones pasadas       │
└─────────────────────┬───────────────────────────────┘
                      │ MCP obsidian-vault
┌─────────────────────▼───────────────────────────────┐
│           ⚙️  CAPA 2 — RAZONAMIENTO                 │
│                    Claude                            │
│        Decide · Orquesta · Estructura resultados     │
│        Tool use · Memoria persistente                │
└──────────┬──────────────────────────┬───────────────┘
           │ FastAPI                  │ Tool calls
┌──────────▼──────────────────────────▼───────────────┐
│           🦾  CAPA 3 — EJECUCIÓN                    │
│              Python + APIs externas                  │
│   PostgreSQL · Redis · Web APIs · Archivos · Código  │
└─────────────────────────────────────────────────────┘
```

---

## Fases

| Fase | Descripción | Estado |
|------|-------------|--------|
| **1 — Fundación** | Infra base: PostgreSQL + pgvector, Redis, config, logging | 🟡 En progreso |
| **2 — Agentes** | Herramientas personalizadas que Claude invoca (tool use) | ⬜ Pendiente |
| **3 — RAG** | Búsqueda semántica sobre notas de Obsidian via pgvector | ⬜ Pendiente |
| **4 — Automatización** | Pipelines que se disparan solos (hooks, schedulers) | ⬜ Pendiente |
| **5 — Interfaz** | Dashboard web para controlarlo todo | ⬜ Pendiente |

---

## Regla de diseño

Antes de construir cualquier componente, pregunta:

1. **¿Qué sabe el sistema aquí?** → Obsidian
2. **¿Qué decide hacer?** → Claude (razonamiento)
3. **¿Cómo lo ejecuta en el mundo real?** → Python + APIs

Arquitecturas limpias, modulares, sin magia oculta.
