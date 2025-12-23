"""API routes and middleware"""

from .routes import router
from .middleware import setup_middleware

__all__ = ["router", "setup_middleware"]
