from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.events import router as event_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(event_router, prefix="/api/events")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
def read_api_health():
    return {"status":"OK"} 