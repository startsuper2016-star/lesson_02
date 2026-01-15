# app/schemas/consultation.py
from pydantic import BaseModel
from typing import Optional, List, Dict


class ConsultationRequest(BaseModel):
    """问诊请求"""
    session_id: Optional[str] = None
    user_input: str


class ConsultationResponse(BaseModel):
    """问诊响应"""
    session_id: str
    bot_response: str
    current_phase: str
    collected_fields: List[str]
    missing_fields: List[str]
    is_complete: bool
    emergency_flag: bool
    medical_record: Optional[Dict] = None
