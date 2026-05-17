# J.A.R.V.I.S — Sistema Operativo de IA Personal

> Sistema modular, local-first, construido sobre Claude + Obsidian

## Visión

JARVIS-OS es un sistema de IA personal que evoluciona en 5 fases: desde infraestructura base hasta inteligencia contextual completa con interfaz de voz. No es un chatbot. Es un sistema operativo cognitivo.

## Fases de Arquitectura

| Fase | Estado | Descripción |
|------|--------|-------------|
| FASE 1 — Fundación | 🟡 En progreso | PostgreSQL + pgvector, Redis, configuración base, logging |
| FASE 2 — Inteligencia Core | ⬜ Pendiente | Motor de memoria, RAG, conversación con contexto |
| FASE 3 — Automatización | ⬜ Pendiente | Hooks, disparadores, agentes autónomos |
| FASE 4 — Voz | ⬜ Pendiente | STT/TTS, interfaz de voz |
| FASE 5 — Interfaz | ⬜ Pendiente | Panel web, visualizaciones |

## Stack Tecnológico

- **Entorno**: Python 3.13 + uv
- **LLM**: Claude (Anthropic API)
- **Base de datos**: PostgreSQL 17 + pgvector
- **Caché**: Redis 8
- **Configuración**: pydantic-settings
- **Pruebas**: pytest + pytest-asyncio

## Inicio Rápido — FASE 1

```bash
# 1. Levantar infraestructura
cd fase-1-fundacion
docker compose up -d

# 2. Instalar dependencias
uv sync

# 3. Configurar variables de entorno
cp .env.ejemplo .env
# Editar .env con tu ANTHROPIC_API_KEY

# 4. Ejecutar pruebas
uv run pytest
```

## Estructura del Proyecto

```
JARVIS-OS/
├── fase-1-fundacion/      # Infraestructura base
│   ├── compartido/        # Configuración, logger, utilidades
│   ├── servicios/         # Servicios (memoria, conocimiento)
│   ├── pruebas/           # Pruebas unitarias
│   ├── docker-compose.yml
│   └── pyproject.toml
├── fase-2-core/           # Motor de inteligencia (próximo)
├── fase-3-automatizacion/ # Automatización (futuro)
├── fase-4-voz/            # Interfaz de voz (futuro)
├── fase-5-interfaz/       # Panel web (futuro)
└── docs/                  # Documentación
```

---

*Construido con Claude Code · zoiket00*
