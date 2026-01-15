# tests/models/test_medical_record.py
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models.medical_record import (
    ChiefComplaint,
    PresentIllness,
    PastHistory,
    MedicalRecord
)


def test_chief_complaint_valid():
    """测试有效的主诉创建"""
    complaint = ChiefComplaint(
        symptom="头痛",
        duration="3天",
        severity=7,
        body_part="左侧颞部"
    )
    assert complaint.symptom == "头痛"
    assert complaint.severity == 7


def test_chief_complaint_severity_validation():
    """测试严重程度范围验证"""
    # 有效范围
    ChiefComplaint(symptom="发热", duration="1天", severity=1)
    ChiefComplaint(symptom="发热", duration="1天", severity=10)

    # 超出范围
    with pytest.raises(ValidationError):
        ChiefComplaint(symptom="发热", duration="1天", severity=0)

    with pytest.raises(ValidationError):
        ChiefComplaint(symptom="发热", duration="1天", severity=11)


def test_present_illness_optional_fields():
    """测试现病史可选字段"""
    illness = PresentIllness()
    assert illness.onset_time is None
    assert illness.progression is None

    illness = PresentIllness(
        associated_symptoms=["恶心", "呕吐"]
    )
    assert len(illness.associated_symptoms) == 2


def test_past_history_allergies():
    """测试既往史过敏记录"""
    history = PastHistory(allergies=["青霉素", "磺胺类药物"])
    assert "青霉素" in history.allergies


def test_medical_record_complete():
    """测试完整医疗记录"""
    record = MedicalRecord(
        session_id="test-session-123",
        timestamp=datetime.now(),
        chief_complaint=ChiefComplaint(
            symptom="胸痛",
            duration="2小时"
        ),
        emergency_flag=True
    )
    assert record.session_id == "test-session-123"
    assert record.emergency_flag is True
