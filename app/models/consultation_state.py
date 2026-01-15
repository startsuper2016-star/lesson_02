# app/models/consultation_state.py
from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Phase(Enum):
    """问诊阶段枚举"""
    GREETING = "greeting"
    CHIEF_COMPLAINT = "chief_complaint"
    PRESENT_ILLNESS = "present_illness"
    PAST_HISTORY = "past_history"
    PERSONAL_HISTORY = "personal_history"
    FAMILY_HISTORY = "family_history"
    REPRODUCTIVE_HISTORY = "reproductive_history"
    REVIEW = "review"
    COMPLETE = "complete"


class ConsultationState(BaseModel):
    """问诊会话状态"""
    session_id: str
    current_phase: Phase = Field(default=Phase.GREETING)
    collected_data: Dict = Field(default_factory=dict)
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
    conflict_history: List[Dict] = Field(default_factory=list)
    emotion_state: str = Field(default="normal")
    emergency_flag: bool = Field(default=False)
    emergency_assessment: Optional[str] = None
    conversation_history: List[str] = Field(default_factory=list)
    last_update: datetime = Field(default_factory=datetime.now)
