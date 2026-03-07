"""
Pydantic Schemas for API Request/Response Validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class PatientBase(BaseModel):
    patient_id: str = Field(..., description="Unique patient identifier")
    name: str = Field(..., min_length=1, max_length=200)
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = Field(None, regex="^(male|female|other)$")
    medical_history: Optional[str] = None


class PatientCreate(PatientBase):
    pass


class PatientResponse(PatientBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class VitalSignsInput(BaseModel):
    patient_id: int = Field(..., description="Patient database ID")
    heart_rate: float = Field(..., ge=0, le=300, description="Heart rate in BPM")
    blood_pressure_systolic: float = Field(..., ge=0, le=300, description="Systolic BP in mmHg")
    blood_pressure_diastolic: float = Field(..., ge=0, le=200, description="Diastolic BP in mmHg")
    oxygen_saturation: float = Field(..., ge=0, le=100, description="SpO2 percentage")
    temperature: float = Field(..., ge=30, le=45, description="Body temperature in Celsius")
    respiratory_rate: float = Field(..., ge=0, le=60, description="Breaths per minute")
    
    @validator('blood_pressure_systolic')
    def validate_bp_systolic(cls, v, values):
        if 'blood_pressure_diastolic' in values and v < values['blood_pressure_diastolic']:
            raise ValueError('Systolic BP must be greater than diastolic BP')
        return v


class VitalSignsResponse(VitalSignsInput):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    id: int
    patient_id: int
    alert_type: str
    severity: str
    message: str
    anomaly_score: Optional[float]
    acknowledged: bool
    acknowledged_by: Optional[str]
    acknowledged_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class AnomalyDetectionResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    confidence: float
    alert_generated: bool
    message: str