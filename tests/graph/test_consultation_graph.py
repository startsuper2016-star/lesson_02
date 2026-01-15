# tests/graph/test_consultation_graph.py
import pytest
from app.models.consultation_state import ConsultationState, Phase
from app.graph.consultation_graph import ConsultationGraph


def test_graph_initialization():
    """测试图初始化"""
    graph = ConsultationGraph()
    assert graph is not None


def test_greeting_node():
    """测试欢迎节点"""
    graph = ConsultationGraph()
    state = ConsultationState(session_id="test-123")

    result = graph.run_greeting(state)
    assert result.current_phase == Phase.CHIEF_COMPLAINT
    assert len(result.conversation_history) > 0


def test_collect_chief_complaint_node():
    """测试收集主诉节点"""
    graph = ConsultationGraph()
    state = ConsultationState(
        session_id="test-456",
        current_phase=Phase.CHIEF_COMPLAINT
    )
    state.conversation_history.append("我头痛三天了")

    result = graph.run_collect_chief_complaint(state)
    assert "chief_complaint" in result.collected_data


def test_emergency_detection():
    """测试紧急检测"""
    graph = ConsultationGraph()
    state = ConsultationState(
        session_id="test-789",
        current_phase=Phase.CHIEF_COMPLAINT
    )
    state.conversation_history.append("我胸痛，呼吸困难")

    result = graph.run_emergency_check(state)
    assert result.emergency_flag is True


def test_phase_transition():
    """测试阶段转换"""
    graph = ConsultationGraph()
    state = ConsultationState(
        session_id="test-abc",
        current_phase=Phase.GREETING
    )

    # 完成欢迎后应进入主诉收集
    next_phase = graph.get_next_phase(state)
    assert next_phase == Phase.CHIEF_COMPLAINT


def test_complete_session():
    """测试完整会话流程"""
    graph = ConsultationGraph()
    state = ConsultationState(session_id="test-complete")

    # 模拟完整对话
    state = graph.run_greeting(state)
    assert state.current_phase == Phase.CHIEF_COMPLAINT

    # 模拟完成所有阶段
    state.current_phase = Phase.COMPLETE
    is_complete = graph.is_complete(state)
    assert is_complete is True
