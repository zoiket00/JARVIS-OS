# J.A.R.V.I.S OS — Personal AI Operating System

Sistema operativo de inteligencia artificial personal construido para **Luis David Ibarra**. Una plataforma autónoma que integra Claude AI con infraestructura de backend, bases de datos vectoriales, interfaces de voz y automatización — diseñada para razonar, recordar y actuar de forma independiente.

> *"Just A Rather Very Intelligent System"*

---

## Tabla de Contenidos

- [Visión del Proyecto](#visión-del-proyecto)
- [Roadmap por Fases](#roadmap-por-fases)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Inicio Rápido](#inicio-rápido)
- [Variables de Entorno](#variables-de-entorno)
- [API Reference](#api-reference)
- [Arquitectura](#arquitectura)
- [Tests](#tests)

---

## Visión del Proyecto

JARVIS OS no es un chatbot — es un sistema operativo de IA personal. Mientras los asistentes convencionales solo responden preguntas, JARVIS:

- **Razona** sobre tareas complejas con acceso a contexto personal
- **Recuerda** usando memoria persistente con vectores semánticos (pgvector)
- **Actúa** de forma autónoma sobre el sistema, el calendario y las aplicaciones
- **Habla** con voz sintetizada usando Whisper + ElevenLabs
- **Aprende** del historial de interacciones del usuario

---

## Roadmap por Fases

| Fase | Nombre | Estado |
|------|--------|--------|
| **Fase 1** | Foundation — Infraestructura base | 🟢 En progreso |
| **Fase 2** | Core AI Engine — Motor de razonamiento | 🔵 Pendiente |
| **Fase 3** | Automation Engine — Automatización de tareas | 🔵 Pendiente |
| **Fase 4** | Voice Engine — Interfaz de voz completa | 🔵 Pendiente |
| **Fase 5** | Interface God Tier — UI definitiva | 🔵 Pendiente |

### Fase 1 — Foundation (Actual)

- [x] Estructura base del proyecto
- [x] API FastAPI con endpoints de chat y streaming SSE
- [x] Integración con Claude (Anthropic SDK) + prompt caching efímero
- [x] Fallback local con Ollama (qwen2.5:7b)
- [x] PostgreSQL 17 + extensión pgvector
- [x] Redis 8 para caché y gestión de sesiones
- [x] Arquitectura async/await completa (asyncio)
- [x] Logging estructurado por módulo
- [ ] Dashboard web (Next.js)
- [ ] Gestión de memoria con embeddings

---

## Stack Tecnológico

| Capa | Tecnología | Detalle |
|------|-----------|---------|
| **LLM Principal** | Claude (Anthropic) | Razonamiento primario + prompt caching |
| **LLM Fallback** | Ollama (qwen2.5:7b) | Local, sin internet requerido |
| **Backend** | Python 3.13 + FastAPI | Async completo, uvicorn |
| **Base de datos** | PostgreSQL 17 + pgvector | Historial + embeddings semánticos |
| **Caché / Sesiones** | Redis 8 | Contexto de conversación activa |
| **Infraestructura** | Docker Compose | PostgreSQL + Redis containerizados |
| **Frontend** | Next.js + React + Tailwind | Dashboard de control (Fase 5) |
| **Voz STT** | Whisper (Groq) | Speech-to-text (Fase 4) |
| **Voz TTS** | ElevenLabs / Piper | Text-to-speech (Fase 4) |
| **Automatización** | n8n + MCP | Workflows y agentes (Fase 3) |
| **Paquetes** | uv | Gestor de paquetes Python rápido |

---

## Estructura del Proyecto

```
JARVIS-OS/
├── fase-1-foundation/              ← Fase activa
│   ├── core/
│   │   └── engine.py               Motor AI: streaming, prompt caching, sesiones
│   ├── interface/
│   │   ├── api.py                  FastAPI app: CORS, middleware, rutas
│   │   └── routes/                 Endpoints organizados por dominio
│   ├── shared/
│   │   ├── config.py               Configuración central (env vars, Pydantic)
│   │   └── logging.py              Logger estructurado por módulo
│   ├── agents/                     Agentes autónomos (Fase 2)
│   ├── automation/                 Motor de automatización (Fase 3)
│   ├── voice/                      Interfaz de voz (Fase 4)
│   ├── memory/                     Gestión de contexto y memoria semántica
│   ├── docker/
│   │   └── docker-compose.yml      PostgreSQL 17 + Redis 8
│   ├── tests/                      Suite de tests (pytest)
│   └── pyproject.toml              Dependencias Python (uv)
└── docs/                           Documentación por fase
```

---

## Inicio Rápido

### Prerequisitos

- **Python** ≥ 3.13
- **uv** — `pip install uv`
- **Docker + Docker Compose**
- **API key de Anthropic**

### 1. Clonar e instalar

```bash
git clone <repo-url>
cd JARVIS-OS/fase-1-foundation
uv sync
```

### 2. Variables de entorno

```bash
cp .env.example .env
# Edita .env con tus API keys
```

### 3. Levantar infraestructura

```bash
docker compose up -d
# Levanta PostgreSQL 17 + Redis 8
```

### 4. Iniciar la API

```bash
# Desarrollo con hot reload
uvicorn interface.api:app --reload --port 8000
```

### 5. Verificar

```bash
curl http://localhost:8000/health
# → {"status": "ok", "timestamp": "..."}
```

---

## Variables de Entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `ANTHROPIC_API_KEY` | API key de Anthropic para Claude | Sí |
| `OLLAMA_BASE_URL` | URL de Ollama local (default: `http://localhost:11434`) | No |
| `POSTGRES_URL` | Connection string PostgreSQL | Sí (prod) |
| `REDIS_URL` | Connection string Redis | No |
| `LOG_LEVEL` | Nivel de logging: `DEBUG` / `INFO` / `WARNING` | No |

---

## API Reference

Todos los endpoints requieren que el servidor esté activo en `http://localhost:8000`.

### Chat

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/health` | Estado del servicio y conexiones |
| `POST` | `/api/chat` | Chat con streaming SSE (token a token) |
| `POST` | `/api/chat/simple` | Chat sin streaming, respuesta completa |

#### `POST /api/chat` — Streaming

```json
{
  "message": "¿Cuál es el estado de mi día?",
  "session_id": "uuid-opcional"
}
```

**Response:** Server-Sent Events con tokens en tiempo real.

#### `POST /api/chat/simple`

```json
{
  "message": "Resume esto: ...",
  "session_id": "uuid-opcional"
}
```

**Response:**
```json
{
  "response": "Texto completo de la respuesta",
  "session_id": "uuid",
  "tokens_used": 420
}
```

---

## Arquitectura

```
Usuario
  │
  ▼
FastAPI  ─── /api/chat ──────────────────────────────────────────┐
  │          /api/chat/simple                                     │
  │          /health                                              │
  ▼                                                               │
Core Engine (engine.py)                                           │
  │                                                               │
  ├── Claude API ─── Anthropic SDK + prompt caching efímero ◄────┘
  │      │
  └── Ollama ──── Fallback local (sin internet)
          │
          ▼
    Capa de memoria
  ├── PostgreSQL + pgvector ──── Historial + embeddings semánticos
  └── Redis ─────────────────── Caché de sesión activa
```

### Decisiones de diseño

| Decisión | Razón |
|----------|-------|
| **Prompt caching efímero** | Reduce tokens y latencia en conversaciones largas. El system prompt se cachea en Claude por 5 min |
| **Async completo** | Todo el stack usa `asyncio` — sin bloqueos síncronos, máximo throughput |
| **Fallback automático** | Si Claude no responde, Ollama toma el relevo localmente sin interrumpir al usuario |
| **pgvector** | Búsqueda semántica sobre historial sin un vector store externo adicional |
| **uv** | 10–100x más rápido que pip para instalar dependencias |

---

## Tests

```bash
# Correr todos los tests
pytest

# Con reporte de cobertura
pytest --cov=. --cov-report=term-missing

# Tests específicos
pytest tests/test_api.py -v
```

---

## Documentación Extendida

Arquitectura completa, roadmap detallado y decisiones de diseño en el vault de Obsidian:

```
c:\Claude - Obsidian\Dios de la IA\proyectos\JARVIS-OS\
```

---

<div align="center">
  <p>Construido por Luis David Ibarra · Powered by Claude + FastAPI + pgvector</p>
</div>
