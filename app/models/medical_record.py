# app/models/medical_record.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChiefComplaint(BaseModel):
    """主诉"""
    symptom: str
    duration: str
    severity: Optional[int] = Field(None, ge=1, le=10)
    body_part: Optional[str] = None


class PresentIllness(BaseModel):
    """现病史"""
    onset_time: Optional[str] = None
    progression: Optional[str] = None
    aggravating_factors: Optional[List[str]] = None
    relieving_factors: Optional[List[str]] = None
    associated_symptoms: Optional[List[str]] = None


class PastHistory(BaseModel):
    """既往史"""
    chronic_diseases: Optional[List[str]] = None
    surgeries: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None


class PersonalHistory(BaseModel):
    """个人史"""
    smoking: Optional[str] = None  # never/former/current
    drinking: Optional[str] = None
    occupation: Optional[str] = None


class FamilyHistory(BaseModel):
    """家族史"""
    hereditary_diseases: Optional[List[str]] = None
    notes: Optional[str] = None


class ReproductiveHistory(BaseModel):
    """生育史"""
    applicable: bool
    details: Optional[str] = None


class MedicalRecord(BaseModel):
    """完整医疗记录"""
    session_id: str
    timestamp: datetime
    chief_complaint: Optional[ChiefComplaint] = None
    present_illness: Optional[PresentIllness] = None
    past_history: Optional[PastHistory] = None
    personal_history: Optional[PersonalHistory] = None
    family_history: Optional[FamilyHistory] = None
    reproductive_history: Optional[ReproductiveHistory] = None
    confidence_scores: dict = Field(default_factory=dict)
    emergency_flag: bool = False
    emergency_recommendation: Optional[str] = None
