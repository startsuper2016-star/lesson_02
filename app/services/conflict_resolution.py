# app/services/conflict_resolution.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict


class ConflictRisk(Enum):
    """冲突风险等级"""
    HIGH = "high"     # 高风险：必须立即确认（如过敏史）
    MEDIUM = "medium" # 中风险：需要澄清
    LOW = "low"       # 低风险：记录但不中断


@dataclass
class Conflict:
    """冲突信息"""
    field: str
    existing_value: str
    new_value: str
    risk: ConflictRisk


class ConflictResolutionService:
    """冲突解决服务"""

    # 高风险字段
    HIGH_RISK_FIELDS = ["allergies", "past_history", "medications"]

    # 矛盾指示词
    CONTRADICTION_INDICATORS = [
        "不是", "不对", "没有", "无", "否",
        "其实", "应该是", "准确说是"
    ]

    def detect(self, existing_data: Dict, new_input: str, field_name: str) -> Optional[Conflict]:
        """
        检测冲突

        Args:
            existing_data: 已采集的数据
            new_input: 新输入
            field_name: 字段名

        Returns:
            冲突对象，无冲突返回 None
        """
        if field_name not in existing_data:
            return None

        existing_value = str(existing_data[field_name])

        # 简单冲突检测：检查是否包含矛盾指示词
        has_contradiction = any(
            indicator in new_input
            for indicator in self.CONTRADICTION_INDICATORS
        )

        if not has_contradiction:
            return None

        # 确定风险等级
        if field_name in self.HIGH_RISK_FIELDS:
            risk = ConflictRisk.HIGH
        elif "symptom" in field_name or "duration" in field_name:
            risk = ConflictRisk.MEDIUM
        else:
            risk = ConflictRisk.LOW

        return Conflict(
            field=field_name,
            existing_value=existing_value,
            new_value=new_input,
            risk=risk
        )

    def generate_backtrack_message(self, conflict: Conflict) -> str:
        """
        生成回溯确认消息

        Args:
            conflict: 冲突对象

        Returns:
            确认消息
        """
        if conflict.risk == ConflictRisk.HIGH:
            return f"抱歉，我需要确认一下。刚才您提到{conflict.existing_value}，现在又说{conflict.new_value}。请问哪个是准确的？这对您的安全很重要。"

        if conflict.risk == ConflictRisk.MEDIUM:
            return f"我注意到您刚才的说法有些不一致。之前说{conflict.existing_value}，现在是{conflict.new_value}。能帮我确认一下吗？"

        return ""

    def should_interrupt(self, conflict: Conflict) -> bool:
        """
        判断是否应该中断流程

        Args:
            conflict: 冲突对象

        Returns:
            True 表示应该中断
        """
        return conflict.risk in [ConflictRisk.HIGH, ConflictRisk.MEDIUM]
