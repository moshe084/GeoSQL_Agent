"""API routes for the Geo-SQL Agent"""

from fastapi import APIRouter, HTTPException, Request, Depends
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

from app.models.schemas import (
    QueryRequest,
    QueryResponse,
    HealthResponse,
    SchemaResponse,
    TableInfo,
    ErrorResponse
)
from app.services.query_service import get_query_service
from app.services.database import get_db_service
from app.config import get_settings
from app import __version__

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/",
    summary="Root endpoint",
    description="Get API information and available endpoints",
    tags=["Info"]
)
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.app_name,
        "version": __version__,
        "environment": settings.environment,
        "endpoints": {
            "/": "GET - API information",
            "/health": "GET - Health check",
            "/schema": "GET - Database schema information",
            "/query": "POST - Execute natural language query",
            "/docs": "GET - Interactive API documentation",
            "/redoc": "GET - Alternative API documentation"
        },
        "documentation": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "openapi_json": "/openapi.json"
        }
    }


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the service and database are healthy",
    tags=["Info"]
)
async def health_check():
    """Health check endpoint"""
    try:
        db_service = get_db_service()
        db_healthy = db_service.health_check()

        if not db_healthy:
            raise HTTPException(
                status_code=503,
                detail="Database connection failed"
            )

        return HealthResponse(
            status="healthy",
            database="connected",
            version=__version__,
            environment=settings.environment
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Health check failed: {str(e)}"
        )


@router.get(
    "/schema",
    response_model=SchemaResponse,
    summary="Get database schema",
    description="Get information about available tables and their structure",
    tags=["Database"]
)
async def get_schema():
    """Get database schema information"""
    try:
        db_service = get_db_service()
        tables_info = db_service.get_schema_info()

        # Convert to Pydantic models
        tables = {}
        total_records = 0

        for table_name, info in tables_info.items():
            tables[table_name] = TableInfo(**info)
            total_records += info["count"]

        return SchemaResponse(
            tables=tables,
            total_records=total_records
        )

    except Exception as e:
        logger.error(f"Failed to get schema: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve schema: {str(e)}"
        )


@router.post(
    "/query",
    response_model=QueryResponse,
    summary="Execute natural language query",
    description="Convert natural language question to SQL and execute it",
    tags=["Query"],
    responses={
        200: {
            "description": "Query executed successfully",
            "model": QueryResponse
        },
        400: {
            "description": "Invalid input or SQL validation failed",
            "model": ErrorResponse
        },
        429: {
            "description": "Too many requests - rate limit exceeded"
        },
        500: {
            "description": "Internal server error during query execution",
            "model": ErrorResponse
        }
    }
)
@limiter.limit(f"{settings.rate_limit_requests}/{settings.rate_limit_period}second")
async def execute_query(
    request: Request,
    query_request: QueryRequest
):
    """
    Execute a natural language query

    This endpoint converts a natural language question into a PostGIS SQL query,
    executes it, and returns the results with GeoJSON geometries.

    Example questions:
    - "Find all cafes within 200 meters of the largest park"
    - "Show all parks larger than 5000 square meters"
    - "What is the closest cafe to the smallest park?"
    """
    try:
        query_service = get_query_service()
        result = await query_service.process_query(query_request)
        return result

    except ValueError as e:
        # Validation errors (invalid SQL, blocked keywords, etc.)
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        # Unexpected errors
        logger.error(f"Query execution error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Query execution failed: {str(e)}"
        )
