# tests/services/test_session_manager.py
import pytest
import time
from datetime import datetime, timedelta
from app.models.consultation_state import ConsultationState, Phase
from app.services.session_manager import SessionManager


def test_create_new_session():
    """测试创建新会话"""
    manager = SessionManager(timeout_minutes=30)
    state = manager.get_or_create(None)
    assert state.session_id is not None
    assert state.current_phase == Phase.GREETING
    assert len(state.conversation_history) == 0


def test_get_existing_session():
    """测试获取已有会话"""
    manager = SessionManager()
    state1 = manager.get_or_create(None)
    session_id = state1.session_id

    # 修改状态
    state1.current_phase = Phase.CHIEF_COMPLAINT
    manager.update(session_id, state1)

    # 获取同一会话
    state2 = manager.get_or_create(session_id)
    assert state2.session_id == session_id
    assert state2.current_phase == Phase.CHIEF_COMPLAINT


def test_session_auto_cleanup():
    """测试会话自动清理"""
    # 使用超短的过期时间进行测试
    manager = SessionManager(timeout_minutes=0)
    state = manager.get_or_create(None)

    # 等待超过过期时间
    time.sleep(1)

    # 尝试获取同一会话 ID，应创建新会话
    new_state = manager.get_or_create(state.session_id)
    # 会话应该已被清理，创建新的
    assert new_state.session_id != state.session_id


def test_update_nonexistent_session():
    """测试更新不存在的会话（应正常创建）"""
    manager = SessionManager()
    new_state = ConsultationState(session_id="nonexistent-123")
    manager.update("nonexistent-123", new_state)

    retrieved = manager.get_or_create("nonexistent-123")
    assert retrieved.session_id == "nonexistent-123"


def test_session_last_update_refreshed():
    """测试获取会话时刷新最后更新时间"""
    manager = SessionManager()
    state1 = manager.get_or_create(None)
    original_time = state1.last_update

    time.sleep(0.1)
    state2 = manager.get_or_create(state1.session_id)

    # 最后更新时间应该被刷新
    assert state2.last_update > original_time
