"""FastAPI Application Entry Point."""

from fastapi import FastAPI

from app.api import health, consultation

app = FastAPI(
    title="医疗问诊 AI 系统",
    description="基于 FastAPI + LangGraph 的智能问诊系统",
    version="1.0.0",
)

# 注册路由
app.include_router(health.router, tags=["health"])
app.include_router(consultation.router, tags=["consultation"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "医疗问诊 AI 系统", "version": "1.0.0"}
