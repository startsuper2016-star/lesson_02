# tests/services/test_emergency_detection.py
import pytest
from app.services.detection.emergency_detection import EmergencyDetectionService, EmergencyLevel


def test_detect_red_flag_chest_pain():
    """测试检测胸痛红色预警"""
    service = EmergencyDetectionService()
    result = service.detect("我感觉胸口很疼，呼吸困难")
    assert result.level == EmergencyLevel.RED
    assert result.is_emergency is True


def test_detect_red_flag_consciousness():
    """测试检测意识模糊红色预警"""
    service = EmergencyDetectionService()
    result = service.detect("我爸意识有点模糊叫不醒")
    assert result.level == EmergencyLevel.RED


def test_detect_yellow_flag_high_fever():
    """测试检测高热黄色预警"""
    service = EmergencyDetectionService()
    result = service.detect("发烧40度已经两天了")
    assert result.level == EmergencyLevel.YELLOW


def test_detect_green_flag():
    """测试检测普通症状绿色预警"""
    service = EmergencyDetectionService()
    result = service.detect("有点咳嗽，流鼻涕")
    assert result.level == EmergencyLevel.GREEN
    assert result.is_emergency is False


def test_get_recommendation_red():
    """测试红色预警建议"""
    service = EmergencyDetectionService()
    result = service.detect("胸痛")
    assert "急诊" in result.recommendation or "紧急" in result.recommendation


def test_get_recommendation_yellow():
    """测试黄色预警建议"""
    service = EmergencyDetectionService()
    result = service.detect("高烧不退")
    assert "尽快" in result.recommendation or "医院" in result.recommendation


def test_no_emergency_mild_symptoms():
    """测试轻微症状无紧急情况"""
    service = EmergencyDetectionService()
    result = service.detect("有点头痛，但不严重")
    assert result.is_emergency is False
