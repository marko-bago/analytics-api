from typing import List
import asyncio
from massive.service import runner
from celery_app import celery_app

@celery_app.task
def start_ws_ingestion(symbols: List[str]):
    asyncio.run(runner(symbols))