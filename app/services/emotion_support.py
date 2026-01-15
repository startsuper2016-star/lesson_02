# app/services/emotion_support.py
from enum import Enum
from typing import List


class EmotionLevel(Enum):
    """情绪等级"""
    NORMAL = "normal"         # 正常
    MILD = "mild"            # 轻度焦虑
    MODERATE = "moderate"    # 中度焦虑
    SEVERE = "severe"        # 重度痛苦


class EmotionSupportService:
    """情感支持服务"""

    # 轻度焦虑关键词
    MILD_KEYWORDS = ["担心", "有点怕", "紧张"]

    # 中度焦虑关键词
    MODERATE_KEYWORDS = ["害怕", "焦虑", "不安", "很担心"]

    # 重度痛苦关键词
    SEVERE_KEYWORDS = ["太害怕了", "恐惧", "整晚睡不着", "一直在哭", "崩溃"]

    def detect_emotion_level(self, text: str) -> EmotionLevel:
        """
        检测情绪等级

        Args:
            text: 用户输入文本

        Returns:
            情绪等级
        """
        # 检查重度
        if any(keyword in text for keyword in self.SEVERE_KEYWORDS):
            return EmotionLevel.SEVERE

        # 检查中度
        if any(keyword in text for keyword in self.MODERATE_KEYWORDS):
            return EmotionLevel.MODERATE

        # 检查轻度
        if any(keyword in text for keyword in self.MILD_KEYWORDS):
            return EmotionLevel.MILD

        return EmotionLevel.NORMAL

    def generate_response(self, level: EmotionLevel, context: str) -> str:
        """
        生成共情回应

        Args:
            level: 情绪等级
            context: 上下文信息（如症状）

        Returns:
            共情回应文本
        """
        if level == EmotionLevel.SEVERE:
            return "我理解您现在一定很痛苦。请先不要着急，深呼吸几次。我们慢慢来，您愿意和我多说一点吗？"

        if level == EmotionLevel.MODERATE:
            return "我理解这种担心，很多人在身体不舒服时都会有类似的感觉。让我们一起梳理一下情况，好吗？"

        if level == EmotionLevel.MILD:
            return "我理解，这确实让人担心。我们继续了解一些信息，可以更好地帮助您。"

        return ""

    def should_slow_pacing(self, responses_times: List[float]) -> bool:
        """
        判断是否应该放慢节奏

        Args:
            responses_times: 最近几次回复的时间间隔（秒）

        Returns:
            True 表示应该放慢
        """
        if not responses_times:
            return False

        avg_time = sum(responses_times) / len(responses_times)
        return avg_time < 1.0  # 平均回复时间小于1秒

    def should_prompt_user(self, last_response_time: float, current_time: float) -> bool:
        """
        判断是否应该催促用户

        Args:
            last_response_time: 上次回复时间戳
            current_time: 当前时间戳

        Returns:
            True 表示应该催促
        """
        elapsed = current_time - last_response_time
        return elapsed > 120  # 超过2分钟无响应
