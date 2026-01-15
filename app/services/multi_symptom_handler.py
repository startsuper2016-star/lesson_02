# app/services/multi_symptom_handler.py
from typing import List
from app.models.consultation_state import ConsultationState


class MultiSymptomHandler:
    """多症状分叉流程处理器"""

    # 症状优先级映射（数字越小优先级越高）
    SYMPTOM_PRIORITY = {
        "胸痛": 1,
        "呼吸困难": 1,
        "意识模糊": 1,
        "大出血": 1,
        "头痛": 2,
        "腹痛": 2,
        "发热": 3,
        "咳嗽": 3,
        "恶心": 3,
        "呕吐": 3,
    }

    # 默认优先级（未知症状）
    DEFAULT_PRIORITY = 99

    # 症状同义词映射
    SYMPTOM_SYNONYMS = {
        "肚子不舒服": "腹痛",
        "肚子痛": "腹痛",
        "拉肚子": "腹泻",
        "发烧": "发热",
    }

    def extract_symptoms(self, text: str) -> List[str]:
        """
        从用户输入中提取症状

        Args:
            text: 用户输入文本

        Returns:
            症状列表
        """
        symptoms = []

        # 检查已知症状
        for symptom in self.SYMPTOM_PRIORITY.keys():
            if symptom in text:
                symptoms.append(symptom)

        # 检查同义词
        for synonym, standard in self.SYMPTOM_SYNONYMS.items():
            if synonym in text and standard not in symptoms:
                symptoms.append(standard)

        return symptoms

    def prioritize(self, symptoms: List[str]) -> List[str]:
        """
        按优先级排序症状

        Args:
            symptoms: 症状列表

        Returns:
            排序后的症状列表
        """
        return sorted(
            symptoms,
            key=lambda s: self.SYMPTOM_PRIORITY.get(s, self.DEFAULT_PRIORITY)
        )

    def create_fork(self, state: ConsultationState, symptoms: List[str]) -> None:
        """
        创建多症状采集分支

        Args:
            state: 会话状态
            symptoms: 检测到的症状列表
        """
        if not symptoms:
            return

        prioritized = self.prioritize(symptoms)

        # 主症状是优先级最高的
        primary = prioritized[0]
        # 其余为次症状
        secondary = prioritized[1:] if len(prioritized) > 1 else []

        state.collected_data["primary_symptom"] = primary
        state.collected_data["secondary_symptoms"] = secondary
