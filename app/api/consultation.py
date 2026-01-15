# app/api/consultation.py
from fastapi import APIRouter, HTTPException, status
from app.schemas.consultation import ConsultationRequest, ConsultationResponse
from app.services.core.session_manager import SessionManager
from app.services.support.input_sanitization import InputSanitizationService
from app.services.detection.emergency_detection import EmergencyDetectionService
from app.services.analysis.structured_extraction import StructuredExtractionService
from app.services.support.emotion_support import EmotionSupportService
from app.services.detection.conflict_resolution import ConflictResolutionService
from app.models.consultation_state import Phase


router = APIRouter(prefix="/api/v1/consultation", tags=["consultation"])

# 初始化服务
session_manager = SessionManager()
sanitization_service = InputSanitizationService()
emergency_service = EmergencyDetectionService()
extraction_service = StructuredExtractionService()
emotion_service = EmotionSupportService()
conflict_service = ConflictResolutionService()


def get_missing_fields(state) -> list:
    """获取缺失字段"""
    required = ["chief_complaint", "present_illness", "past_history"]
    collected = state.collected_data.keys()
    return [f for f in required if f not in collected]


@router.post("/chat", response_model=ConsultationResponse)
async def chat(request: ConsultationRequest):
    """
    主对话接口

    处理用户输入，返回机器人响应
    """
    # 输入验证
    if not sanitization_service.validate_input(request.user_input):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="输入包含不安全内容"
        )

    # 获取或创建会话
    state = session_manager.get_or_create(request.session_id)

    # 敏感信息脱敏
    cleaned_input, detected = sanitization_service.sanitize(request.user_input)

    # 添加用户输入
    state.conversation_history.append(f"用户: {cleaned_input}")

    # 紧急检测
    emergency_result = emergency_service.detect(cleaned_input)
    state.emergency_flag = emergency_result.is_emergency

    if emergency_result.is_emergency:
        state.emergency_assessment = emergency_result.recommendation
        state.current_phase = Phase.COMPLETE
        bot_response = emergency_result.recommendation
    else:
        # 根据当前阶段生成响应
        bot_response = _generate_response_for_phase(state, cleaned_input)

    state.conversation_history.append(f"助手: {bot_response}")

    # 更新会话
    session_manager.update(state.session_id, state)

    return ConsultationResponse(
        session_id=state.session_id,
        bot_response=bot_response,
        current_phase=state.current_phase.value,
        collected_fields=list(state.collected_data.keys()),
        missing_fields=get_missing_fields(state),
        is_complete=state.current_phase == Phase.COMPLETE,
        emergency_flag=state.emergency_flag,
        medical_record=state.collected_data if state.current_phase == Phase.COMPLETE else None
    )


def _generate_response_for_phase(state, user_input: str) -> str:
    """根据阶段生成响应"""
    phase = state.current_phase

    if phase == Phase.GREETING:
        state.current_phase = Phase.CHIEF_COMPLAINT
        return "您好，请问您有什么不舒服？"

    elif phase == Phase.CHIEF_COMPLAINT:
        # 简单提取主诉
        if "头痛" in user_input or "痛" in user_input:
            state.collected_data["chief_complaint"] = {"symptom": user_input}
            state.current_phase = Phase.PRESENT_ILLNESS
            return "请问这个症状持续多久了？有没有其他伴随症状？"

        return "请问主要是什么症状？"

    elif phase == Phase.PRESENT_ILLNESS:
        state.collected_data["present_illness"] = {"notes": user_input}
        state.current_phase = Phase.PAST_HISTORY
        return "请问您既往有什么病史吗？比如高血压、糖尿病等。"

    elif phase == Phase.PAST_HISTORY:
        state.collected_data["past_history"] = {"notes": user_input}
        state.current_phase = Phase.COMPLETE
        return "问诊已完成，感谢您的配合。"

    return "请问还有什么可以帮您的？"


@router.get("/medical-record/{session_id}")
async def get_medical_record(session_id: str):
    """
    获取预问诊病历

    仅在会话完成后可获取
    """
    state = session_manager.get(session_id)

    if not state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在"
        )

    if state.current_phase != Phase.COMPLETE:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话未完成"
        )

    return state.collected_data
