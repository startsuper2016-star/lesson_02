# app/services/session_manager.py
from datetime import datetime, timedelta
from typing import Dict, Optional
import uuid
from app.models.consultation_state import ConsultationState


class SessionManager:
    """内存会话管理器，支持自动过期清理"""

    def __init__(self, timeout_minutes: int = 30):
        """
        初始化会话管理器

        Args:
            timeout_minutes: 会话超时时间（分钟）
        """
        self.sessions: Dict[str, ConsultationState] = {}
        self.timeout = timedelta(minutes=timeout_minutes)

    def get_or_create(self, session_id: Optional[str] = None) -> ConsultationState:
        """
        获取或创建会话

        Args:
            session_id: 会话 ID，None 表示创建新会话

        Returns:
            会话状态对象
        """
        self._cleanup_expired()

        if session_id and session_id in self.sessions:
            # 刷新最后更新时间
            self.sessions[session_id].last_update = datetime.now()
            return self.sessions[session_id]

        # 创建新会话
        new_id = session_id or self._generate_id()
        new_state = ConsultationState(session_id=new_id)
        self.sessions[new_id] = new_state
        return new_state

    def update(self, session_id: str, state: ConsultationState) -> None:
        """
        更新会话状态

        Args:
            session_id: 会话 ID
            state: 新的会话状态
        """
        self.sessions[session_id] = state

    def get(self, session_id: str) -> Optional[ConsultationState]:
        """
        获取会话状态（不刷新时间）

        Args:
            session_id: 会话 ID

        Returns:
            会话状态对象，不存在返回 None
        """
        return self.sessions.get(session_id)

    def _cleanup_expired(self) -> None:
        """清理过期会话"""
        now = datetime.now()
        expired = [
            sid for sid, state in self.sessions.items()
            if now - state.last_update > self.timeout
        ]
        for sid in expired:
            del self.sessions[sid]

    def _generate_id(self) -> str:
        """生成唯一会话 ID"""
        return str(uuid.uuid4())
