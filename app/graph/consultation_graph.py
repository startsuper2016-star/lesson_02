# app/graph/consultation_graph.py
from typing import Optional
from app.models.consultation_state import ConsultationState, Phase
from app.services.emergency_detection import EmergencyDetectionService
from app.services.structured_extraction import StructuredExtractionService
from app.services.emotion_support import EmotionSupportService


class ConsultationGraph:
    """问诊状态机"""

    def __init__(self):
        """初始化图"""
        self.emergency_service = EmergencyDetectionService()
        self.extraction_service = StructuredExtractionService()
        self.emotion_service = EmotionSupportService()

    def run_greeting(self, state: ConsultationState) -> ConsultationState:
        """
        欢迎节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        welcome_message = "您好，我是智能问诊助手。我会了解您的一些情况，请如实告诉我您的症状。"
        state.conversation_history.append(f"助手: {welcome_message}")
        state.current_phase = Phase.CHIEF_COMPLAINT
        return state

    def run_collect_chief_complaint(self, state: ConsultationState) -> ConsultationState:
        """
        收集主诉节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        # 从对话历史提取信息
        conversation = "\n".join(state.conversation_history)

        # 提取主诉
        chief_complaint = self.extraction_service.extract(
            conversation,
            "chief_complaint"
        )

        if chief_complaint.get("symptom"):
            state.collected_data["chief_complaint"] = chief_complaint
            # 进入下一阶段
            state.current_phase = Phase.PRESENT_ILLNESS

        return state

    def run_emergency_check(self, state: ConsultationState) -> ConsultationState:
        """
        紧急情况检查节点

        Args:
            state: 当前状态

        Returns:
            更新后的状态
        """
        # 检查最新输入
        if state.conversation_history:
            last_input = state.conversation_history[-1]

            result = self.emergency_service.detect(last_input)
            state.emergency_flag = result.is_emergency

            if result.is_emergency:
                state.emergency_assessment = result.recommendation
                state.current_phase = Phase.COMPLETE

        return state

    def get_next_phase(self, state: ConsultationState) -> Optional[Phase]:
        """
        获取下一阶段

        Args:
            state: 当前状态

        Returns:
            下一阶段，完成返回 None
        """
        phase_order = [
            Phase.GREETING,
            Phase.CHIEF_COMPLAINT,
            Phase.PRESENT_ILLNESS,
            Phase.PAST_HISTORY,
            Phase.PERSONAL_HISTORY,
            Phase.FAMILY_HISTORY,
            Phase.REPRODUCTIVE_HISTORY,
            Phase.REVIEW,
            Phase.COMPLETE
        ]

        try:
            current_index = phase_order.index(state.current_phase)
            if current_index + 1 < len(phase_order):
                return phase_order[current_index + 1]
        except ValueError:
            pass

        return None

    def is_complete(self, state: ConsultationState) -> bool:
        """
        判断会话是否完成

        Args:
            state: 当前状态

        Returns:
            是否完成
        """
        return state.current_phase == Phase.COMPLETE or state.emergency_flag
