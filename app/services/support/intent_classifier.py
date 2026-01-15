# app/services/intent_classifier.py
from enum import Enum


class Intent(Enum):
    """用户意图枚举"""
    RELEVANT_INFO = "relevant_info"       # 提供相关信息
    IRRELEVANT_CHAT = "irrelevant_chat"   # 无关聊天
    QUESTION = "question"                 # 提问
    COMPLAINT = "complaint"               # 抱怨
    EMOTIONAL = "emotional"               # 情绪宣泄


class IntentClassifier:
    """用户意图分类服务"""

    # 问题关键词
    QUESTION_KEYWORDS = ["为什么", "怎么", "什么", "请问", "能否"]

    # 抱怨关键词
    COMPLAINT_KEYWORDS = ["烦", "慢", "多", "麻烦", "啰嗦"]

    # 情绪关键词
    EMOTIONAL_KEYWORDS = ["害怕", "担心", "焦虑", "恐惧", "紧张", "难过"]

    # 无关聊天关键词
    IRRELEVANT_KEYWORDS = ["天气", "吃饭", "睡觉", "周末", "电影"]

    def classify(self, user_input: str) -> Intent:
        """
        分类用户意图

        Args:
            user_input: 用户输入

        Returns:
            意图类别
        """
        # 检测情绪
        if any(keyword in user_input for keyword in self.EMOTIONAL_KEYWORDS):
            return Intent.EMOTIONAL

        # 检测抱怨
        if any(keyword in user_input for keyword in self.COMPLAINT_KEYWORDS):
            return Intent.COMPLAINT

        # 检测问题
        if any(keyword in user_input for keyword in self.QUESTION_KEYWORDS):
            return Intent.QUESTION

        # 检测无关聊天
        if any(keyword in user_input for keyword in self.IRRELEVANT_KEYWORDS):
            return Intent.IRRELEVANT_CHAT

        # 默认：相关信息
        return Intent.RELEVANT_INFO
