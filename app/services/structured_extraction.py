# app/services/structured_extraction.py
from typing import Dict
import re


class StructuredExtractionService:
    """结构化提取服务"""

    # 术语标准化字典
    TERMINOLOGY_MAP = {
        "感冒": "上呼吸道感染",
        "打针": "注射治疗",
        "挂水": "静脉输液",
        "发烧": "发热",
        "拉肚子": "腹泻",
        "便秘": "排便困难",
    }

    def __init__(self):
        """初始化服务"""
        pass

    def extract(self, conversation: str, field_type: str) -> Dict:
        """
        从对话中提取特定字段

        Args:
            conversation: 对话历史
            field_type: 字段类型（chief_complaint, present_illness 等）

        Returns:
            提取的字段值字典
        """
        if field_type == "chief_complaint":
            return self._extract_chief_complaint(conversation)
        elif field_type == "present_illness":
            return self._extract_present_illness(conversation)
        elif field_type == "past_history":
            return self._extract_past_history(conversation)
        return {}

    def extract_batch(self, conversation: str) -> Dict:
        """
        批量提取所有字段

        Args:
            conversation: 对话历史

        Returns:
            所有提取的字段
        """
        return {
            "chief_complaint": self.extract(conversation, "chief_complaint"),
            "present_illness": self.extract(conversation, "present_illness"),
            "past_history": self.extract(conversation, "past_history"),
        }

    def _extract_chief_complaint(self, conversation: str) -> Dict:
        """提取主诉"""
        result = {"symptom": None, "duration": None, "severity": None}

        # 简单关键词提取
        if "头痛" in conversation:
            result["symptom"] = self._standardize("头痛")
        if "胸痛" in conversation:
            result["symptom"] = self._standardize("胸痛")
        if "腹痛" in conversation:
            result["symptom"] = self._standardize("腹痛")

        # 提取持续时间
        duration_match = re.search(r'(\d+)(天|小时|周)', conversation)
        if duration_match:
            result["duration"] = duration_match.group(0)

        return result

    def _extract_present_illness(self, conversation: str) -> Dict:
        """提取现病史"""
        return {
            "onset_time": None,
            "progression": None,
            "associated_symptoms": []
        }

    def _extract_past_history(self, conversation: str) -> Dict:
        """提取既往史"""
        result = {
            "chronic_diseases": [],
            "surgeries": [],
            "allergies": [],
            "medications": []
        }

        if "高血压" in conversation:
            result["chronic_diseases"].append("高血压")
        if "糖尿病" in conversation:
            result["chronic_diseases"].append("糖尿病")

        return result

    def _validate_age(self, age_str: str) -> bool:
        """验证年龄"""
        try:
            age = int(age_str)
            return 0 <= age <= 150
        except (ValueError, TypeError):
            return False

    def _validate_time(self, time_str: str) -> bool:
        """验证时间描述"""
        future_indicators = ["明天", "后天", "下周", "以后"]
        return not any(indicator in time_str for indicator in future_indicators)

    def _standardize(self, term: str) -> str:
        """标准化医学术语"""
        return self.TERMINOLOGY_MAP.get(term, term)
