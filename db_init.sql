CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

CREATE TABLE IF NOT EXISTS ticks (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    ts TIMESTAMPTZ NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    size BIGINT,
    exchange TEXT
);

-- Create hypertable on ts
SELECT create_hypertable('ticks', 'ts', if_not_exists => TRUE);