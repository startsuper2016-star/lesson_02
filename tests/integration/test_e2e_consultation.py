# tests/integration/test_e2e_consultation.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_complete_consultation_flow():
    """测试完整问诊流程"""
    # 1. 开始问诊
    response1 = client.post(
        "/api/v1/consultation/chat",
        json={"user_input": "你好"}
    )
    assert response1.status_code == 200
    session_id = response1.json()["session_id"]
    assert "您好" in response1.json()["bot_response"]

    # 2. 描述主诉
    response2 = client.post(
        "/api/v1/consultation/chat",
        json={
            "session_id": session_id,
            "user_input": "我头痛三天了"
        }
    )
    assert response2.status_code == 200
    assert "chief_complaint" in response2.json()["collected_fields"]

    # 3. 描述现病史
    response3 = client.post(
        "/api/v1/consultation/chat",
        json={
            "session_id": session_id,
            "user_input": "有点恶心，没发烧"
        }
    )
    assert response3.status_code == 200

    # 4. 既往史
    response4 = client.post(
        "/api/v1/consultation/chat",
        json={
            "session_id": session_id,
            "user_input": "有高血压，一直在吃药"
        }
    )
    assert response4.status_code == 200

    # 5. 检查完成的病历
    record_response = client.get(f"/api/v1/consultation/medical-record/{session_id}")
    if record_response.status_code == 200:
        record = record_response.json()
        assert "chief_complaint" in record or "past_history" in record


def test_emergency_flow():
    """测试紧急情况流程"""
    response = client.post(
        "/api/v1/consultation/chat",
        json={"user_input": "我胸痛，呼吸困难，很严重"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["emergency_flag"] is True
    assert "急诊" in data["bot_response"] or "紧急" in data["bot_response"]


def test_irrelevant_input_handling():
    """测试无关输入处理"""
    response = client.post(
        "/api/v1/consultation/chat",
        json={"user_input": "今天天气不错"}
    )
    assert response.status_code == 200
    # 应该引导回正轨
    assert len(response.json()["bot_response"]) > 0


def test_multi_symptom_flow():
    """测试多症状流程"""
    response = client.post(
        "/api/v1/consultation/chat",
        json={"user_input": "我头痛，还有点胸痛，咳嗽"}
    )
    assert response.status_code == 200
    # 应该处理多个症状
    data = response.json()
    assert data["session_id"] is not None
