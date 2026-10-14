-- Script de creación de la tabla única para el historial de conversaciones.
-- Ejecutar manualmente: sqlite3 data/app.db < sql/schema.sql

CREATE TABLE IF NOT EXISTS mensajes (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id   VARCHAR(64)  NOT NULL,
    role              VARCHAR(20)  NOT NULL,  -- 'user' | 'assistant' | 'system'
    content           TEXT         NOT NULL,
    archivos          TEXT,                   -- JSON con lista de archivos adjuntos
    grafico           TEXT,                   -- JSON con especificación del gráfico (opcional)
    created_at        DATETIME     DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS ix_mensajes_conversation_id
    ON mensajes (conversation_id);