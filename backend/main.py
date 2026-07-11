import logging
import os

from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import test_database_connection
from app.core.redis import test_redis_connection

logger = logging.getLogger(__name__)

is_production = os.getenv("APP_ENV") == "production"

app = FastAPI(
    title="Matrimony API",
    version="1.0.0",
    docs_url=None if is_production else "/docs",
    redoc_url=None if is_production else "/redoc",
    openapi_url=None if is_production else "/openapi.json",
)


@app.get("/")
async def root():
    return {
        "status": "success",
        "message": "Matrimony API is running",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }


@app.get("/health/redis")
async def health_redis():
    redis_connected = await test_redis_connection()

    response = {
        "status": "healthy" if redis_connected else "unhealthy",
        "services": {
            "api": "connected",
            "redis": "connected" if redis_connected else "disconnected",
        },
    }

    if not redis_connected:
        return{
            "status_code":status.HTTP_503_SERVICE_UNAVAILABLE,
            "content":response,
        }

    return response


@app.get("/health/database")
def database_health():
    try:
        test_database_connection()

        return {
            "status": "healthy",
            "database": "connected",
        }

    except SQLAlchemyError:
        logger.exception("PostgreSQL health check failed")

        return {
            "status_code": 503,
            "content": {
                "status": "unhealthy",
                "database": "disconnected",
            },
        }
