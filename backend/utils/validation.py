"""
Pydantic Validation Schemas

Defines validation schemas for agent inputs and outputs to ensure type safety
and data integrity throughout the MetaMind pipeline.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


# Enums for constrained values
class Domain(str, Enum):
    """Valid application domains."""
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    ECOMMERCE = "ecommerce"
    EDUCATION = "education"
    LEGAL = "legal"
    GENERAL = "general"


class Modality(str, Enum):
    """Valid data modalities."""
    TEXT = "text"
    VISION = "vision"
    MULTIMODAL = "multimodal"
    TABULAR = "tabular"


class RiskTolerance(str, Enum):
    """Valid risk tolerance levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ComplianceLevel(str, Enum):
    """Valid compliance levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Topology(str, Enum):
    """Valid architecture topologies."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"


# Input validation schemas
class ConstraintsInput(BaseModel):
    """Validation schema for system constraints."""
    budget: float = Field(..., gt=0, description="Monthly budget in USD")
    latency_target_ms: int = Field(..., gt=0, le=10000, description="Target latency in milliseconds")
    expected_users: int = Field(..., gt=0, description="Expected concurrent users")
    risk_tolerance: RiskTolerance = Field(..., description="Risk tolerance level")
    compliance_level: ComplianceLevel = Field(..., description="Compliance level required")
    
    @field_validator('budget')
    @classmethod
    def validate_budget(cls, v):
        """Ensure budget is reasonable."""
        if v > 1000000:
            raise ValueError("Budget exceeds reasonable limit of $1M/month")
        return v
    
    @field_validator('expected_users')
    @classmethod
    def validate_users(cls, v):
        """Ensure user count is reasonable."""
        if v > 10000000:
            raise ValueError("Expected users exceeds reasonable limit of 10M")
        return v


class RequirementInput(BaseModel):
    """Validation schema for requirement agent input."""
    business_goal: str = Field(..., min_length=10, max_length=500, description="Clear business objective")
    domain: Domain = Field(..., description="Application domain")
    modalities: List[Modality] = Field(..., min_items=1, description="Data modalities to handle")
    constraints: ConstraintsInput = Field(..., description="System constraints")
    
    @field_validator('business_goal')
    @classmethod
    def validate_business_goal(cls, v):
        """Ensure business goal is meaningful."""
        if len(v.split()) < 3:
            raise ValueError("Business goal must be at least 3 words")
        return v


class WeightsOutput(BaseModel):
    """Validation schema for optimization weights."""
    cost: float = Field(..., ge=0, le=1, description="Cost weight")
    latency: float = Field(..., ge=0, le=1, description="Latency weight")
    risk: float = Field(..., ge=0, le=1, description="Risk weight")
    compliance: float = Field(..., ge=0, le=1, description="Compliance weight")
    scalability: float = Field(..., ge=0, le=1, description="Scalability weight")
    complexity: float = Field(..., ge=0, le=1, description="Complexity weight")
    
    @model_validator(mode='after')
    def validate_weights_sum(self):
        """Ensure weights sum to 1.0."""
        total = sum([
            self.cost,
            self.latency,
            self.risk,
            self.compliance,
            self.scalability,
            self.complexity
        ])
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {total}")
        return self


class ArchitectureModuleSchema(BaseModel):
    """Validation schema for architecture module."""
    layer: str = Field(..., min_length=1, description="Architecture layer")
    component: str = Field(..., min_length=1, description="Component name")
    config: Dict[str, Any] = Field(default_factory=dict, description="Component configuration")


class ArchitectureSchema(BaseModel):
    """Validation schema for architecture."""
    architecture_id: str = Field(..., description="Unique architecture ID")
    name: str = Field(..., min_length=1, max_length=200, description="Architecture name")
    template: str = Field(..., description="Template used")
    modules: List[ArchitectureModuleSchema] = Field(..., min_items=1, description="Architecture modules")
    topology: Topology = Field(..., description="Architecture topology")
    estimated_metrics: Optional[Dict[str, float]] = Field(None, description="Estimated metrics")
    final_score: Optional[float] = Field(None, ge=0, le=100, description="Final score")


class MetricsOutput(BaseModel):
    """Validation schema for normalized metrics."""
    cost: float = Field(..., ge=0, le=100, description="Cost score (0-100)")
    latency: float = Field(..., ge=0, le=100, description="Latency score (0-100)")
    risk: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    compliance: float = Field(..., ge=0, le=100, description="Compliance score (0-100)")
    scalability: float = Field(..., ge=0, le=100, description="Scalability score (0-100)")
    complexity: float = Field(..., ge=0, le=100, description="Complexity score (0-100)")


class ReflectionOutput(BaseModel):
    """Validation schema for reflection feedback."""
    confidence_score: float = Field(..., ge=0, le=1, description="Confidence score (0.0-1.0)")
    strengths: List[str] = Field(default_factory=list, description="Architecture strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Architecture weaknesses")
    improvement_suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    should_iterate: bool = Field(..., description="Whether to iterate")
    
    @field_validator('confidence_score')
    @classmethod
    def validate_confidence(cls, v):
        """Ensure confidence is in valid range."""
        if v < 0 or v > 1:
            raise ValueError("Confidence score must be between 0.0 and 1.0")
        return v


class VersionRecord(BaseModel):
    """Validation schema for version record."""
    version: int = Field(..., ge=1, description="Version number")
    timestamp: str = Field(..., description="ISO-8601 timestamp")
    architecture_id: str = Field(..., description="Architecture ID")
    score: float = Field(..., ge=0, le=100, description="Architecture score")
    changes_made: List[str] = Field(default_factory=list, description="Changes applied")
    parent_version: Optional[int] = Field(None, ge=1, description="Parent version number")


class ComparisonOutput(BaseModel):
    """Validation schema for version comparison."""
    version_1: int = Field(..., ge=1, description="First version number")
    version_2: int = Field(..., ge=1, description="Second version number")
    score_delta: float = Field(..., description="Score difference")
    metric_deltas: Dict[str, float] = Field(..., description="Metric differences")
    improvements: List[str] = Field(default_factory=list, description="Improvements made")
    regressions: List[str] = Field(default_factory=list, description="Regressions found")
    recommendation: str = Field(..., description="Recommendation")


# Validation helper functions
def validate_state_constraints(state: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate state constraints.
    
    Args:
        state: State dictionary to validate
        
    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []
    
    try:
        # Validate constraints if present
        if "constraints" in state:
            ConstraintsInput(**state["constraints"])
    except Exception as e:
        errors.append(f"Invalid constraints: {str(e)}")
    
    try:
        # Validate weights if present
        if "weights" in state:
            WeightsOutput(**state["weights"])
    except Exception as e:
        errors.append(f"Invalid weights: {str(e)}")
    
    try:
        # Validate architectures if present
        if "candidate_architectures" in state:
            for arch in state["candidate_architectures"]:
                ArchitectureSchema(**arch)
    except Exception as e:
        errors.append(f"Invalid architecture: {str(e)}")
    
    return len(errors) == 0, errors


def validate_metrics(metrics: Dict[str, float]) -> tuple[bool, List[str]]:
    """
    Validate metrics are in correct range.
    
    Args:
        metrics: Metrics dictionary
        
    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []
    
    try:
        MetricsOutput(**metrics)
    except Exception as e:
        errors.append(f"Invalid metrics: {str(e)}")
    
    return len(errors) == 0, errors


def validate_reflection(reflection: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate reflection feedback.
    
    Args:
        reflection: Reflection dictionary
        
    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []
    
    try:
        ReflectionOutput(**reflection)
    except Exception as e:
        errors.append(f"Invalid reflection: {str(e)}")
    
    return len(errors) == 0, errors