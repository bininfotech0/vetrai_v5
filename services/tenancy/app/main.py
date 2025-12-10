"""
Tenancy Service - VetrAI Platform

Handles organization management and multi-tenant support.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from pathlib import Path

# Add shared modules to path
sys.path.append(str(Path(__file__).parent.parent))

from shared.config import get_settings
from routes import router as tenancy_router

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="VetrAI Tenancy Service",
    description="Organization management and multi-tenant support for VetrAI Platform",
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting Tenancy Service...")
    logger.info(f"Environment: {settings.environment}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down Tenancy Service...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "VetrAI Tenancy Service",
        "version": settings.api_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include routers
app.include_router(tenancy_router, prefix=f"/api/{settings.api_version}", tags=["tenancy"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=settings.log_level.lower())
