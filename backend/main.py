import logging
import os

from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import test_database_connection

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
            "status_code":503,
            "content":{
                "status": "unhealthy",
                "database": "disconnected",
            },
        }
