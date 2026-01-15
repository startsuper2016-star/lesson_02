# tests/services/test_conflict_resolution.py
import pytest
from app.services.detection.conflict_resolution import ConflictResolutionService, ConflictRisk, Conflict


def test_detect_allergy_conflict():
    """测试检测过敏史冲突（高风险）"""
    service = ConflictResolutionService()
    existing = {"allergies": "无过敏史"}
    new_input = "我对青霉素过敏"

    conflict = service.detect(existing, new_input, "allergies")
    assert conflict is not None
    assert conflict.risk == ConflictRisk.HIGH


def test_detect_symptom_conflict():
    """测试检测症状描述冲突（中风险）"""
    service = ConflictResolutionService()
    existing = {"symptom_duration": "已经一周了"}
    new_input = "就今天才开始痛"

    conflict = service.detect(existing, new_input, "symptom_duration")
    assert conflict is not None
    assert conflict.risk == ConflictRisk.MEDIUM


def test_no_conflict_consistent():
    """测试一致信息无冲突"""
    service = ConflictResolutionService()
    existing = {"symptom": "头痛"}
    new_input = "是的，头痛，很痛"

    conflict = service.detect(existing, new_input, "symptom")
    assert conflict is None


def test_generate_backtrack_message_high_risk():
    """测试生成高风险回溯消息"""
    service = ConflictResolutionService()
    conflict = Conflict(
        field="allergies",
        existing_value="无过敏史",
        new_value="对青霉素过敏",
        risk=ConflictRisk.HIGH
    )
    message = service.generate_backtrack_message(conflict)
    assert "刚才" in message
    assert "现在" in message
    assert "青霉素" in message


def test_generate_backtrack_message_medium_risk():
    """测试生成中风险回溯消息"""
    service = ConflictResolutionService()
    conflict = Conflict(
        field="duration",
        existing_value="一周",
        new_value="今天",
        risk=ConflictRisk.MEDIUM
    )
    message = service.generate_backtrack_message(conflict)
    assert len(message) > 0


def test_low_risk_no_interruption():
    """测试低风险不中断流程"""
    service = ConflictResolutionService()
    conflict = Conflict(
        field="detail",
        existing_value="有点疼",
        new_value="不是很疼",
        risk=ConflictRisk.LOW
    )
    should_interrupt = service.should_interrupt(conflict)
    assert should_interrupt is False
