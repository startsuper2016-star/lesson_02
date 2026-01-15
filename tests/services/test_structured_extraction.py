# tests/services/test_structured_extraction.py
import pytest
from app.services.structured_extraction import StructuredExtractionService


def test_extract_chief_complaint():
    """测试提取主诉"""
    service = StructuredExtractionService()
    conversation = "用户: 我头痛\n助手: 请问持续多久了？\n用户: 三天了"

    result = service.extract(conversation, "chief_complaint")
    assert result["symptom"] == "头痛"
    assert "duration" in result


def test_extract_with_missing_info():
    """测试信息缺失时的处理"""
    service = StructuredExtractionService()
    conversation = "用户: 我不太舒服"

    result = service.extract(conversation, "present_illness")
    # 缺失信息应为 None 或空，不应编造
    assert result.get("onset_time") is None or result.get("onset_time") == ""


def test_rule_validation_age():
    """测试规则引擎年龄验证"""
    service = StructuredExtractionService()
    # 正常年龄
    assert service._validate_age("35") is True
    # 异常年龄
    assert service._validate_age("200") is False
    assert service._validate_age("-5") is False


def test_rule_validation_time():
    """测试规则引擎时间验证"""
    service = StructuredExtractionService()
    # 正常时间
    assert service._validate_time("3天前") is True
    assert service._validate_time("2小时") is True
    # 异常时间（未来时间）
    assert service._validate_time("明天") is False


def test_terminology_standardization():
    """测试术语标准化"""
    service = StructuredExtractionService()
    assert service._standardize("感冒") == "上呼吸道感染"
    assert service._standardize("打针") == "注射治疗"
    assert service._standardize("头痛") == "头痛"  # 无需标准化


def test_extract_batch():
    """测试批量提取"""
    service = StructuredExtractionService()
    conversation = """
    用户: 我头痛三天了，有点恶心
    用户: 以前有高血压，吃药
    """

    result = service.extract_batch(conversation)
    assert "chief_complaint" in result
    assert "past_history" in result
