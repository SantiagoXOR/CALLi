-- Create campaigns table
CREATE TABLE IF NOT EXISTS campaigns (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    schedule_start TIMESTAMP WITH TIME ZONE,
    schedule_end TIMESTAMP WITH TIME ZONE,
    contact_list_ids INTEGER[] DEFAULT '{}',
    script_template TEXT,
    max_retries INTEGER NOT NULL DEFAULT 3,
    retry_delay_minutes INTEGER NOT NULL DEFAULT 60,
    total_calls INTEGER NOT NULL DEFAULT 0,
    successful_calls INTEGER NOT NULL DEFAULT 0,
    failed_calls INTEGER NOT NULL DEFAULT 0,
    pending_calls INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on status for faster filtering
CREATE INDEX idx_campaigns_status ON campaigns(status);

-- Create index on schedule_start for faster date-based queries
CREATE INDEX idx_campaigns_schedule ON campaigns(schedule_start);

-- Add row level security policies
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;

-- Policy for selecting campaigns
CREATE POLICY "Users can view their own campaigns" ON campaigns
    FOR SELECT
    USING (auth.uid() = ANY (contact_list_ids));

-- Policy for inserting campaigns
CREATE POLICY "Users can create campaigns" ON campaigns
    FOR INSERT
    WITH CHECK (auth.uid() IS NOT NULL);

-- Policy for updating campaigns
CREATE POLICY "Users can update their own campaigns" ON campaigns
    FOR UPDATE
    USING (auth.uid() = ANY (contact_list_ids));

-- Policy for deleting campaigns
CREATE POLICY "Users can delete their own campaigns" ON campaigns
    FOR DELETE
    USING (auth.uid() = ANY (contact_list_ids));
