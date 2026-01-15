# app/services/confidence_scoring.py
from typing import Dict


class ConfidenceScoringService:
    """置信度评分服务"""

    # 模糊关键词
    UNCERTAIN_KEYWORDS = ["可能", "大概", "好像", "似乎", "不太确定"]

    # 明确关键词
    CERTAIN_KEYWORDS = ["确实", "已经", "一直", "肯定", "一定"]

    def score(self, text: str, field_name: str) -> float:
        """
        为单个字段评分

        Args:
            text: 字段文本值
            field_name: 字段名称

        Returns:
            置信度分数 (0.0 - 1.0)
        """
        # 空值
        if not text or not text.strip():
            return 0.0

        # 包含明确关键词
        if any(keyword in text for keyword in self.CERTAIN_KEYWORDS):
            return 0.9

        # 包含模糊关键词
        if any(keyword in text for keyword in self.UNCERTAIN_KEYWORDS):
            return 0.6

        # 根据文本长度判断
        if len(text.strip()) >= 5:
            return 0.85

        return 0.7

    def get_confidence_level(self, score: float) -> str:
        """
        获取置信度等级

        Args:
            score: 置信度分数

        Returns:
            等级字符串: "high", "medium", "low"
        """
        if score >= 0.8:
            return "high"
        elif score >= 0.5:
            return "medium"
        else:
            return "low"

    def score_batch(self, data: Dict[str, str]) -> Dict[str, float]:
        """
        批量评分

        Args:
            data: 字段名到值的映射

        Returns:
            字段名到置信度分数的映射
        """
        return {
            field_name: self.score(value, field_name)
            for field_name, value in data.items()
        }
