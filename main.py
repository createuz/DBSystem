from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db, dispose_db
from logger import logger
from redis_client import init_redis, close_redis
from routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    logger.info("✅ Application startup complete")
    yield
    await dispose_db()
    await close_redis()
    logger.info("🛑 Application shutdown complete")


app = FastAPI(
    title="Social Media API",
    version="1.0",
    lifespan=lifespan
)

app.include_router(users.router)


@app.get("/")
async def health():
    return {"status": "ok"}
