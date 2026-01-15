# tests/models/test_consultation_state.py
import pytest
from datetime import datetime
from app.models.consultation_state import ConsultationState, Phase


def test_phase_enum_values():
    """测试阶段枚举值正确"""
    assert Phase.GREETING.value == "greeting"
    assert Phase.CHIEF_COMPLAINT.value == "chief_complaint"
    assert Phase.COMPLETE.value == "complete"


def test_consultation_state_creation():
    """测试会话状态创建"""
    state = ConsultationState(session_id="test-123")
    assert state.session_id == "test-123"
    assert state.current_phase == Phase.GREETING
    assert state.collected_data == {}
    assert state.emergency_flag is False


def test_consultation_state_with_initial_data():
    """测试带初始数据的会话状态"""
    state = ConsultationState(
        session_id="test-456",
        current_phase=Phase.CHIEF_COMPLAINT,
        emotion_state="anxious"
    )
    assert state.current_phase == Phase.CHIEF_COMPLAINT
    assert state.emotion_state == "anxious"


def test_conversation_history_append():
    """测试对话历史追加"""
    state = ConsultationState(session_id="test-789")
    state.conversation_history.append("用户: 我头痛")
    assert len(state.conversation_history) == 1
    assert "头痛" in state.conversation_history[0]
