-- JARVIS-OS — Inicialización de base de datos
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Conversaciones: memoria persistente entre sesiones
CREATE TABLE IF NOT EXISTS conversaciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sesion_id TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('usuario', 'asistente', 'sistema')),
    contenido TEXT NOT NULL,
    metadatos JSONB DEFAULT '{}',
    embedding vector(1536),
    creado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Nodos de conocimiento: información estructurada
CREATE TABLE IF NOT EXISTS nodos_conocimiento (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo TEXT NOT NULL,
    contenido TEXT NOT NULL,
    fuente TEXT,
    etiquetas TEXT[] DEFAULT '{}',
    embedding vector(1536),
    metadatos JSONB DEFAULT '{}',
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para búsqueda vectorial por similitud (HNSW)
CREATE INDEX IF NOT EXISTS idx_conversaciones_embedding
    ON conversaciones USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_conocimiento_embedding
    ON nodos_conocimiento USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_conversaciones_sesion
    ON conversaciones (sesion_id, creado_en DESC);
