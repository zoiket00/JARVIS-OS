# J.A.R.V.I.S — Personal AI Operating System

> Sistema operativo de IA personal — modular, local-first, construido sobre Claude + Obsidian

## Vision

JARVIS-OS es un sistema de IA personal que evoluciona en 5 fases desde infraestructura base hasta una interfaz de voz e inteligencia contextual completa. No es un chatbot. Es un sistema operativo cognitivo.

## Arquitectura por Fases

| Fase | Estado | Descripción |
|------|--------|-------------|
| FASE 1 — Foundation | 🟡 En progreso | PostgreSQL + pgvector, Redis, config base, logging |
| FASE 2 — Core Intelligence | ⬜ Pendiente | Memory engine, RAG, conversación con contexto |
| FASE 3 — Automation | ⬜ Pendiente | Hooks, triggers, agentes autónomos |
| FASE 4 — Voice | ⬜ Pendiente | STT/TTS, interfaz de voz |
| FASE 5 — Interface | ⬜ Pendiente | Dashboard web, visualizaciones |

## Stack Tecnológico

- **Runtime**: Python 3.13 + uv
- **LLM**: Claude (Anthropic API)
- **Base de datos**: PostgreSQL 17 + pgvector
- **Cache**: Redis 8
- **Config**: pydantic-settings
- **Tests**: pytest + pytest-asyncio

## Inicio Rápido — FASE 1

```bash
# 1. Levantar infraestructura
cd fase-1-foundation
docker compose up -d

# 2. Instalar dependencias
uv sync

# 3. Configurar variables
cp .env.example .env
# Editar .env con tu ANTHROPIC_API_KEY

# 4. Correr tests
uv run pytest
```

## Estructura

```
JARVIS-OS/
├── fase-1-foundation/     # Infraestructura base
│   ├── shared/            # Config, logger, utilidades compartidas
│   ├── services/          # Servicios (memory, knowledge)
│   ├── tests/             # Tests unitarios
│   ├── docker-compose.yml
│   └── pyproject.toml
├── fase-2-core/           # Motor de inteligencia (próximo)
├── fase-3-automation/     # Automatización (futuro)
├── fase-4-voice/          # Interfaz de voz (futuro)
├── fase-5-interface/      # Dashboard web (futuro)
└── docs/                  # Documentación
```

---

*Construido con Claude Code | zoiket00*
