
from massive.websocket.models import WebSocketMessage
from typing import List, Tuple
import logging
from asyncpg import Connection
from datetime import datetime, timezone
from db.session import get_connection, init_db

from massive import WebSocketClient
from massive.websocket.models import WebSocketMessage, Feed, Market

from settings import settings

async def batch_store_massive_ticks(conn: Connection, msgs: List[WebSocketMessage]) -> None:

    async def _execute_batch(conn: Connection, batch: List[Tuple]) -> None:

        query = """
        INSERT INTO ticks(symbol, timestamp_utc, timestamp_unix_ms, price, size, exchange)
        VALUES($1, $2, $3, $4, $5, $6)
        """
        await conn.executemany(query, batch)
        logging.info(f"Inserted batch of {len(batch)} ticks")


    batch: List[Tuple[str, datetime, str, int, float, int, str]] = []

    for m in msgs:
        ts_ms = m.data.get("t")
        ts_s: str = m.data.get("t") / 1000 # get seconds
        try:
            ts: datetime = datetime.fromtimestamp(ts_s, tz=timezone.utc)
        except Exception:
            ts = datetime.now(timezone.utc)
        batch.append((
            m.symbol,
            ts,
            ts_ms,
            float(m.data.get("p", 0)),
            int(m.data.get("s", 0)),   
            m.data.get("x")          
        ))

        logging.info(f"Stored tick: {m}")
    
        if len(batch) >= settings.worker_batch_size:
            await _execute_batch(conn, batch)
            batch.clear()

    # execute remaining msgs
    if batch:
        await _execute_batch(conn, batch)


async def runner(symbols: List[str]) -> None:

    await init_db()
    client: WebSocketClient = WebSocketClient(
        api_key=settings.massive_api_key,
        feed=Feed.Delayed,
	    market=Market.Stocks,
        subscriptions=symbols
    )

    async def handle_msg(msgs: List[WebSocketMessage]):
        async with get_connection() as conn:
            await batch_store_massive_ticks(conn, msgs)

    await client.run(handle_msg)