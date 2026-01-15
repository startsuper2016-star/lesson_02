# tests/services/test_confidence_scoring.py
import pytest
from app.services.core.confidence_scoring import ConfidenceScoringService


def test_score_clear_statement():
    """测试明确陈述获得高置信度"""
    service = ConfidenceScoringService()
    score = service.score("我头痛已经三天了", "symptom")
    assert score >= 0.8


def test_score_vague_statement():
    """测试模糊陈述获得低置信度"""
    service = ConfidenceScoringService()
    score = service.score("就是不太舒服", "symptom")
    assert score <= 0.4


def test_score_partial_info():
    """测试部分信息获得中等置信度"""
    service = ConfidenceScoringService()
    score = service.score("可能有点疼吧", "symptom")
    assert 0.5 <= score <= 0.7


def test_score_with_missing_value():
    """测试缺失值获得零置信度"""
    service = ConfidenceScoringService()
    score = service.score("", "symptom")
    assert score == 0.0


def test_get_confidence_level():
    """测试置信度等级获取"""
    service = ConfidenceScoringService()
    assert service.get_confidence_level(0.9) == "high"
    assert service.get_confidence_level(0.6) == "medium"
    assert service.get_confidence_level(0.3) == "low"


def test_score_multiple_fields():
    """测试批量评分"""
    service = ConfidenceScoringService()
    scores = service.score_batch({
        "symptom": "头痛三天",
        "duration": "大概3天吧",
        "severity": ""
    })
    assert scores["symptom"] >= 0.8
    assert 0.5 <= scores["duration"] <= 0.7
    assert scores["severity"] == 0.0
