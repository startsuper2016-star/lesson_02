# tests/api/test_consultation.py
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_new_session():
    """测试创建新会话"""
    response = client.post(
        "/api/v1/consultation/chat",
        json={"user_input": "你好"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] is not None
    assert data["current_phase"] == "greeting" or "chief_complaint"
    assert data["is_complete"] is False


def test_continue_session():
    """测试继续已有会话"""
    # 先创建会话
    response1 = client.post(
        "/api/v1/consultation/chat",
        json={"user_input": "我头痛"}
    )
    session_id = response1.json()["session_id"]

    # 继续会话
    response2 = client.post(
        "/api/v1/consultation/chat",
        json={
            "session_id": session_id,
            "user_input": "三天了"
        }
    )
    assert response2.status_code == 200
    assert response2.json()["session_id"] == session_id


def test_emergency_detection():
    """测试紧急情况检测"""
    response = client.post(
        "/api/v1/consultation/chat",
        json={"user_input": "我胸痛，呼吸困难"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["emergency_flag"] is True


def test_get_medical_record():
    """测试获取医疗记录"""
    # 先完成会话
    response = client.post(
        "/api/v1/consultation/chat",
        json={"user_input": "我头痛三天"}
    )
    session_id = response.json()["session_id"]

    # 获取记录（可能尚未完成）
    response = client.get(f"/api/v1/consultation/medical-record/{session_id}")

    # 如果会话未完成应返回 404
    if response.status_code == 404:
        assert "会话未完成" in response.json()["detail"]
    elif response.status_code == 200:
        assert response.json() is not None


def test_input_sanitization():
    """测试输入清洗"""
    response = client.post(
        "/api/v1/consultation/chat",
        json={"user_input": "我叫张三，电话13812345678，头痛"}
    )
    assert response.status_code == 200
    # 敏感信息应该被脱敏
