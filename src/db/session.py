from contextlib import asynccontextmanager
from typing import Optional
from collections.abc import AsyncGenerator
from ..settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from asyncpg import Pool, create_pool, Connection


conn_pool: Optional[Pool] = None

async def init_db() -> Pool:
    global conn_pool
    conn_pool = await create_pool(settings.database_url, min_size=1, max_size=10)

    async with conn_pool.acquire() as session:
        await session.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
        await session.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            id BIGSERIAL PRIMARY KEY,
            symbol TEXT NOT NULL,
            ts TIMESTAMPTZ NOT NULL,
            price DOUBLE PRECISION NOT NULL,
            size BIGINT,
            exchange TEXT
        );
        """)
        await session.execute("SELECT create_hypertable('ticks', 'ts', if_not_exists => TRUE);")
    return conn_pool

@asynccontextmanager
async def get_connection(self) -> AsyncGenerator[Connection, None]:

    if self.pool is None:
        raise RuntimeError("Pool not initialized. Call init_pool() first.")
    async with self.pool.acquire() as conn:
        yield conn