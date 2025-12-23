"""
Geo-SQL Agent - AI-Powered Spatial Query Engine
Main FastAPI application with best practices
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.api.routes import router
from app.api.middleware import setup_middleware
from app.services.database import get_db_service
from app import __version__

# Configure logging
settings = get_settings()
logging.basicConfig(
    level=settings.log_level,
    format=settings.log_format
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    logger.info("=" * 80)
    logger.info(f"Starting {settings.app_name} v{__version__}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info("=" * 80)

    # Initialize services
    db_service = get_db_service()
    if db_service.health_check():
        logger.info("Database connection verified")
    else:
        logger.error("Database connection failed!")

    logger.info("Application startup complete")

    yield

    # Shutdown
    logger.info("Shutting down application...")
    db_service.close()
    logger.info("Database connections closed")
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="""
    🌍 **AI-Powered Spatial Query Engine**

    Transform natural language questions into PostGIS SQL queries and visualize
    results on an interactive map.

    ## Features

    * 🧠 Natural language to SQL conversion using GPT-4
    * 🗺️ PostGIS spatial queries with geometry support
    * ⚡ Real-time query execution and results
    * 📊 Support for Points, Polygons, and LineStrings
    * 🇮🇱 Hebrew and English language support

    ## Example Queries

    * "Find all cafes within 200 meters of the largest park"
    * "Show all parks larger than 5000 square meters"
    * "מצא תכניות בניין עיר שמכילות בתי קפה"

    ## Database Tables

    * **cafes**: Coffee shops (Points)
    * **parks**: Parks and green spaces (Polygons)
    * **roads**: Streets and roads (LineStrings)
    * **plans**: Israeli urban planning data (Polygons)
    """,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    debug=settings.debug
)

# Setup middleware (CORS, logging, rate limiting)
setup_middleware(app)

# Include routers
app.include_router(router, prefix="")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions"""
    logger.error(f"Uncaught exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.debug else "Internal server error"
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
