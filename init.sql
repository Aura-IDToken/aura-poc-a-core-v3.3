-- Aura PoCA Core Database Initialization
-- PostgreSQL + pgvector (version from pgvector/pgvector:pg16 image)
-- Local-First Sovereign Implementation

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Audit Event Log Table
-- Immutable append-only log for all evaluated events
CREATE TABLE IF NOT EXISTS audit_events (
    id BIGSERIAL PRIMARY KEY,
    agent_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    event_hash VARCHAR(64) NOT NULL UNIQUE,
    merkle_root VARCHAR(64) NOT NULL,
    poca_score DECIMAL(3, 2) NOT NULL CHECK (poca_score >= 0.0 AND poca_score <= 1.0),
    drift DECIMAL(3, 2) NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('COMPLIANT', 'DRIFT', 'FAIL', 'HALTED')),
    raw_event JSONB NOT NULL,
    certificate JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'audit_events_certificate_raw_ari_present_chk'
    ) THEN
        ALTER TABLE audit_events
            ADD CONSTRAINT audit_events_certificate_raw_ari_present_chk
            CHECK (certificate ? 'RAW_ARI');
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'audit_events_certificate_raw_ari_integer_chk'
    ) THEN
        ALTER TABLE audit_events
            ADD CONSTRAINT audit_events_certificate_raw_ari_integer_chk
            CHECK (
                jsonb_typeof(certificate -> 'RAW_ARI') = 'number'
                AND (certificate ->> 'RAW_ARI') ~ '^[0-9]+$'
                AND (certificate ->> 'RAW_ARI')::BIGINT BETWEEN 0 AND 100000
            );
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'audit_events_poca_score_matches_raw_ari_chk'
    ) THEN
        ALTER TABLE audit_events
            ADD CONSTRAINT audit_events_poca_score_matches_raw_ari_chk
            CHECK (
                poca_score = ROUND(
                    (certificate ->> 'RAW_ARI')::NUMERIC / 100000,
                    2
                )
            );
    END IF;
END
$$;

CREATE OR REPLACE FUNCTION prevent_audit_events_mutation()
RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'audit_events is append-only; % is not permitted', TG_OP
        USING ERRCODE = '55000';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER audit_events_append_only
BEFORE UPDATE OR DELETE ON audit_events
FOR EACH ROW
EXECUTE FUNCTION prevent_audit_events_mutation();

-- Create indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_audit_events_agent_id ON audit_events(agent_id);
CREATE INDEX IF NOT EXISTS idx_audit_events_timestamp ON audit_events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_audit_events_status ON audit_events(status);
CREATE INDEX IF NOT EXISTS idx_audit_events_merkle_root ON audit_events(merkle_root);

-- Agent Constitution Table
-- Stores agent constitutions with vector embeddings
CREATE TABLE IF NOT EXISTS agent_constitutions (
    id BIGSERIAL PRIMARY KEY,
    agent_id VARCHAR(255) NOT NULL UNIQUE,
    constitution_text TEXT NOT NULL,
    constitution_hash VARCHAR(64) NOT NULL,
    embedding vector(32),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Kill-Switch State Table
-- Art. 14 Oversight: Manual Emergency Halt
CREATE TABLE IF NOT EXISTS kill_switch_state (
    id SERIAL PRIMARY KEY,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    activated_at TIMESTAMPTZ,
    activated_by VARCHAR(255),
    reason TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Initialize kill-switch as inactive
INSERT INTO kill_switch_state (id, is_active, updated_at)
VALUES (1, FALSE, NOW())
ON CONFLICT (id) DO NOTHING;

-- Policy Violations Log
-- Art. 5 Safeguard: Track algorithmic policy violations
CREATE TABLE IF NOT EXISTS policy_violations (
    id BIGSERIAL PRIMARY KEY,
    agent_id VARCHAR(255) NOT NULL,
    event_hash VARCHAR(64) NOT NULL,
    policy_rule VARCHAR(255) NOT NULL,
    violation_type VARCHAR(50) NOT NULL,
    detected_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    FOREIGN KEY (event_hash) REFERENCES audit_events(event_hash)
);

CREATE INDEX IF NOT EXISTS idx_policy_violations_agent_id ON policy_violations(agent_id);
CREATE INDEX IF NOT EXISTS idx_policy_violations_detected_at ON policy_violations(detected_at DESC);

-- Grant permissions (for local dev environment)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO aura;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO aura;
