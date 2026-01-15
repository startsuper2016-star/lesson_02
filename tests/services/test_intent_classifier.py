# tests/services/test_intent_classifier.py
import pytest
from app.services.support.intent_classifier import IntentClassifier, Intent


def test_classify_relevant_info():
    """测试分类相关信息"""
    classifier = IntentClassifier()
    intent = classifier.classify("我头痛已经三天了")
    assert intent == Intent.RELEVANT_INFO


def test_classify_irrelevant_chat():
    """测试分类无关聊天"""
    classifier = IntentClassifier()
    intent = classifier.classify("今天天气不错啊")
    assert intent == Intent.IRRELEVANT_CHAT


def test_classify_question():
    """测试分类提问"""
    classifier = IntentClassifier()
    intent = classifier.classify("为什么要问我这些？")
    assert intent == Intent.QUESTION


def test_classify_complaint():
    """测试分类抱怨"""
    classifier = IntentClassifier()
    intent = classifier.classify("你们这问题太多了，烦死了")
    assert intent == Intent.COMPLAINT


def test_classify_emotional():
    """测试分类情绪表达"""
    classifier = IntentClassifier()
    intent = classifier.classify("我很害怕，不知道是不是大病")
    assert intent == Intent.EMOTIONAL


def test_classify_edge_case():
    """测试边界情况"""
    classifier = IntentClassifier()
    # 默认分类为相关信息
    intent = classifier.classify("我也不太清楚怎么描述")
    assert intent == Intent.RELEVANT_INFO
