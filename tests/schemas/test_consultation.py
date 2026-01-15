# tests/schemas/test_consultation.py
import pytest
from app.schemas.consultation import ConsultationRequest, ConsultationResponse


def test_consultation_request_new_session():
    """测试新会话请求"""
    request = ConsultationRequest(user_input="我头痛")
    assert request.session_id is None
    assert request.user_input == "我头痛"


def test_consultation_request_existing_session():
    """测试已有会话请求"""
    request = ConsultationRequest(
        session_id="existing-123",
        user_input="还有点恶心"
    )
    assert request.session_id == "existing-123"


def test_consultation_response_complete():
    """测试完整会话响应"""
    response = ConsultationResponse(
        session_id="test-123",
        bot_response="请问头痛持续多久了？",
        current_phase="chief_complaint",
        collected_fields=["symptom"],
        missing_fields=["duration", "severity"],
        is_complete=False,
        emergency_flag=False
    )
    assert response.is_complete is False
    assert len(response.missing_fields) == 2


def test_consultation_response_with_medical_record():
    """测试带医疗记录的响应"""
    response = ConsultationResponse(
        session_id="test-456",
        bot_response="问诊完成",
        current_phase="complete",
        collected_fields=["symptom", "duration"],
        missing_fields=[],
        is_complete=True,
        emergency_flag=False,
        medical_record={"symptom": "头痛", "duration": "3天"}
    )
    assert response.is_complete is True
    assert response.medical_record is not None
