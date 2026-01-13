"""Dependency Injection."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Use this for startup and shutdown events:
    - Startup: Initialize database connections, load models, etc.
    - Shutdown: Close connections, cleanup resources, etc.
    """
    # Startup
    print("Application startup...")
    yield
    # Shutdown
    print("Application shutdown...")


async def get_db():
    """Database session dependency.

    Replace with actual database session when needed.
    """
    # TODO: Implement actual database session
    return None
