import os
from fastapi import FastAPI

is_production = os.getenv('APP_ENV') == "production"

app = FastAPI(
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