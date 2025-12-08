"""
Workers Service - VetrAI Platform
"""

import logging
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

sys.path.append(str(Path(__file__).parent.parent.parent))

from shared.config import get_settings

from .routes import router as workers_router

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VetrAI Workers Service",
    description="Workflow execution and job management service for VetrAI Platform",
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.on_event("startup")
async def startup_event():
    logger.info("Starting Workers Service...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Workers Service...")


@app.get("/")
async def root():
    return {
        "service": "VetrAI Workers Service",
        "version": settings.api_version,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(
    workers_router, prefix=f"/api/{settings.api_version}", tags=["workers"]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=settings.log_level.lower())
