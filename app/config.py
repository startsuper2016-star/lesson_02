# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置"""

    # OpenAI 配置
    openai_api_key: str
    openai_base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-4"

    # 会话配置
    session_timeout_minutes: int = 30
    max_conversation_length: int = 50

    class Config:
        env_file = ".env"
        case_sensitive = False


# 全局配置实例
settings = Settings()
