# tests/services/test_multi_symptom_handler.py
import pytest
from app.services.analysis.multi_symptom_handler import MultiSymptomHandler


def test_extract_single_symptom():
    """测试提取单个症状"""
    handler = MultiSymptomHandler()
    symptoms = handler.extract_symptoms("我头痛")
    assert "头痛" in symptoms


def test_extract_multiple_symptoms():
    """测试提取多个症状"""
    handler = MultiSymptomHandler()
    symptoms = handler.extract_symptoms("我头痛，还有点肚子不舒服，有点咳嗽")
    assert "头痛" in symptoms
    assert "腹痛" in symptoms or "肚子" in "".join(symptoms)


def test_prioritize_symptoms():
    """测试症状优先级排序"""
    handler = MultiSymptomHandler()
    symptoms = ["头痛", "咳嗽", "胸痛"]
    prioritized = handler.prioritize(symptoms)

    # 胸痛优先级最高（1）
    assert prioritized[0] == "胸痛"


def test_prioritize_all_high_priority():
    """测试多个高优先级症状排序"""
    handler = MultiSymptomHandler()
    symptoms = ["胸痛", "呼吸困难", "头痛"]
    prioritized = handler.prioritize(symptoms)

    # 胸痛和呼吸困难应该排在前面
    assert prioritized[0] in ["胸痛", "呼吸困难"]
    assert prioritized[1] in ["胸痛", "呼吸困难"]


def test_unknown_symptom_priority():
    """测试未知症状获得默认低优先级"""
    handler = MultiSymptomHandler()
    symptoms = ["头痛", "手麻"]
    prioritized = handler.prioritize(symptoms)

    # 手麻不在优先级表中，应该排在后面
    assert prioritized[0] == "头痛"
    assert prioritized[1] == "手麻"


def test_create_fork_workflow():
    """测试创建分叉工作流"""
    handler = MultiSymptomHandler()
    from app.models.consultation_state import ConsultationState

    state = ConsultationState(session_id="test-123")
    symptoms = ["胸痛", "头痛"]

    # 创建分叉后，应该设置主症状
    handler.create_fork(state, symptoms)
    assert state.collected_data.get("primary_symptom") == "胸痛"
    assert state.collected_data.get("secondary_symptoms") == ["头痛"]
