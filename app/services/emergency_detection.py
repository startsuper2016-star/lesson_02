# app/services/emergency_detection.py
from enum import Enum
from dataclasses import dataclass
from typing import List


class EmergencyLevel(Enum):
    """紧急程度等级"""
    RED = "red"       # 红色预警：立即急诊
    YELLOW = "yellow" # 黄色预警：尽快就医
    GREEN = "green"   # 绿色预警：常规问诊


@dataclass
class EmergencyDetectionResult:
    """紧急检测结果"""
    is_emergency: bool
    level: EmergencyLevel
    recommendation: str


class EmergencyDetectionService:
    """紧急症状检测服务"""

    # 红色预警关键词
    RED_FLAGS = [
        "胸痛", "胸闷", "心慌",
        "呼吸困难", "呼吸急促", "喘不上气",
        "意识模糊", "昏迷", "昏厥",
        "大出血", "大量出血",
        "剧烈疼痛", "无法忍受"
    ]

    # 黄色预警关键词
    YELLOW_FLAGS = [
        "高热", "高烧", "发烧40度", "发烧39度",
        "严重脱水", "虚脱",
        "持续呕吐", "无法进食"
    ]

    def detect(self, text: str) -> EmergencyDetectionResult:
        """
        检测紧急情况

        Args:
            text: 用户输入文本

        Returns:
            紧急检测结果
        """
        # 检查红色预警
        if self._contains_any(text, self.RED_FLAGS):
            return EmergencyDetectionResult(
                is_emergency=True,
                level=EmergencyLevel.RED,
                recommendation=self._get_red_recommendation()
            )

        # 检查黄色预警
        if self._contains_any(text, self.YELLOW_FLAGS):
            return EmergencyDetectionResult(
                is_emergency=True,
                level=EmergencyLevel.YELLOW,
                recommendation=self._get_yellow_recommendation()
            )

        # 绿色预警（普通情况）
        return EmergencyDetectionResult(
            is_emergency=False,
            level=EmergencyLevel.GREEN,
            recommendation=""
        )

    def _contains_any(self, text: str, keywords: List[str]) -> bool:
        """检查文本是否包含任何关键词"""
        return any(keyword in text for keyword in keywords)

    def _get_red_recommendation(self) -> str:
        """获取红色预警建议"""
        return "您描述的症状需要立即就医，建议您立即前往最近医院的急诊科就诊。如有需要，请拨打120急救电话。"

    def _get_yellow_recommendation(self) -> str:
        """获取黄色预警建议"""
        return "您的情况建议尽快就医，不要拖延。建议您今天内去医院就诊。"
