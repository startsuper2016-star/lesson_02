"""FastAPI Application Entry Point."""

from fastapi import FastAPI

from app.api import health

app = FastAPI(
    title="Lesson 02 API",
    description="FastAPI Backend API",
    version="0.1.0",
)

# Include routers
app.include_router(health.router, tags=["health"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Lesson 02 API"}
