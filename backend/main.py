"""
Backward compatibility shim - imports the actual app from app.main
This file maintains compatibility with existing docker-compose.yml
"""

from app.main import app

__all__ = ["app"]
