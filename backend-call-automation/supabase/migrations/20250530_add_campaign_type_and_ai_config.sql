-- Crear tipo de enumeración para tipos de campaña
CREATE TYPE campaign_type AS ENUM (
    'sales',
    'support',
    'survey',
    'follow_up',
    'educational',
    'retention'
);

-- Añadir columna de tipo de campaña a la tabla campaigns
ALTER TABLE campaigns
ADD COLUMN campaign_type campaign_type NOT NULL DEFAULT 'sales';

-- Añadir columna para configuración de IA (JSON)
ALTER TABLE campaigns
ADD COLUMN ai_config JSONB DEFAULT '{"model": "gpt-4", "temperature": 0.7, "max_tokens": 150, "custom_prompt_variables": {}}';

-- Añadir columna para puntos clave
ALTER TABLE campaigns
ADD COLUMN key_points TEXT[] DEFAULT '{}';

-- Actualizar índices
CREATE INDEX idx_campaigns_campaign_type ON campaigns(campaign_type);

-- Comentarios para documentación
COMMENT ON COLUMN campaigns.campaign_type IS 'Tipo de campaña que determina el comportamiento de la IA';
COMMENT ON COLUMN campaigns.ai_config IS 'Configuración específica para la IA en formato JSON';
COMMENT ON COLUMN campaigns.key_points IS 'Puntos clave a mencionar durante la llamada';
