# tests/services/test_emotion_support.py
import pytest
from app.services.emotion_support import EmotionSupportService, EmotionLevel


def test_detect_normal_emotion():
    """测试检测正常情绪"""
    service = EmotionSupportService()
    level = service.detect_emotion_level("我头痛三天")
    assert level == EmotionLevel.NORMAL


def test_detect_mild_anxiety():
    """测试检测轻度焦虑"""
    service = EmotionSupportService()
    level = service.detect_emotion_level("有点担心这个病")
    assert level == EmotionLevel.MILD


def test_detect_moderate_anxiety():
    """测试检测中度焦虑"""
    service = EmotionSupportService()
    level = service.detect_emotion_level("我很害怕，不知道是不是严重的问题")
    assert level == EmotionLevel.MODERATE


def test_detect_severe_distress():
    """测试检测重度痛苦"""
    service = EmotionSupportService()
    level = service.detect_emotion_level("我太害怕了，整晚都睡不着觉，一直在哭")
    assert level == EmotionLevel.SEVERE


def test_generate_empathy_response_mild():
    """测试轻度情绪共情回应"""
    service = EmotionSupportService()
    response = service.generate_response(EmotionLevel.MILD, "头痛")
    assert len(response) > 0
    assert "理解" in response or "担心" in response


def test_generate_empathy_response_severe():
    """测试重度情绪安抚回应"""
    service = EmotionSupportService()
    response = service.generate_response(EmotionLevel.SEVERE, "")
    # 重度情绪应该优先安抚，不继续问诊
    assert "先不要着急" in response or "深呼吸" in response or "慢慢说" in response


def test_adjust_pacing_rapid_response():
    """测试快节奏调整"""
    service = EmotionSupportService()
    # 模拟快速连续回复
    should_slow = service.should_slow_pacing(
        responses_times=[0.5, 0.3, 0.4, 0.6]
    )
    assert should_slow is True


def test_adjust_pacing_slow_response():
    """测试慢节奏催促"""
    service = EmotionSupportService()
    # 模拟回复很慢
    should_prompt = service.should_prompt_user(
        last_response_time=120, current_time=180
    )
    assert should_prompt is True
