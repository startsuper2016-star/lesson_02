"""Health Check Endpoint."""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

# 增加健康检查路由
@router.get("/")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Service is running"}
