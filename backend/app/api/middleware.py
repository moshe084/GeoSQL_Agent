"""Middleware for rate limiting, CORS, and logging"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import logging
import time
from typing import Callable

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


async def log_requests_middleware(request: Request, call_next: Callable):
    """Log all incoming requests with timing"""
    start_time = time.time()

    # Log request
    logger.info(
        f"Incoming request: {request.method} {request.url.path} "
        f"from {request.client.host if request.client else 'unknown'}"
    )

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Log response
    logger.info(
        f"Request completed: {request.method} {request.url.path} "
        f"status={response.status_code} duration={duration:.3f}s"
    )

    # Add timing header
    response.headers["X-Process-Time"] = str(duration)

    return response


def setup_middleware(app: FastAPI) -> None:
    """Configure all middleware for the application"""

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    logger.info(f"CORS middleware configured with origins: {settings.cors_origins}")

    # Request logging middleware
    app.middleware("http")(log_requests_middleware)
    logger.info("Request logging middleware configured")

    # Rate limiting
    if settings.rate_limit_enabled:
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        logger.info(
            f"Rate limiting enabled: {settings.rate_limit_requests} requests "
            f"per {settings.rate_limit_period} seconds"
        )
