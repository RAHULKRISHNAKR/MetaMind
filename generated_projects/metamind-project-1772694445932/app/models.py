"""
Database Models for Healthcare Monitoring System
"""

from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Patient(Base):
    """Patient information model"""
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    medical_history = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    vital_signs = relationship("VitalSigns", back_populates="patient", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="patient", cascade="all, delete-orphan")


class VitalSigns(Base):
    """Vital signs measurements model"""
    __tablename__ = "vital_signs"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    heart_rate = Column(Float, nullable=False)
    blood_pressure_systolic = Column(Float, nullable=False)
    blood_pressure_diastolic = Column(Float, nullable=False)
    oxygen_saturation = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    respiratory_rate = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="vital_signs")


class Alert(Base):
    """Alert notifications model"""
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    alert_type = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    message = Column(Text, nullable=False)
    anomaly_score = Column(Float)
    acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(String(100))
    acknowledged_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    patient = relationship("Patient", back_populates="alerts")