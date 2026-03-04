"""
MetaMind State Schema

This module defines the state object that flows through the MetaMind
multi-agent architecture design pipeline.
"""

from typing import List, Dict, Optional, Any
from typing_extensions import TypedDict
from datetime import datetime
import uuid


class ArchitectureModule(TypedDict):
    """Single module in an architecture."""
    layer: str  # Data, Preprocessing, Embedding, Model, Tool, Agent, Validation, Monitoring, Deployment
    component: str
    config: Dict[str, Any]


class Architecture(TypedDict):
    """Complete architecture specification."""
    architecture_id: str
    name: str
    template: str
    modules: List[ArchitectureModule]
    topology: str  # sequential, parallel, hierarchical
    estimated_metrics: Optional[Dict[str, float]]
    final_score: Optional[float]


class Constraints(TypedDict):
    """System constraints."""
    budget: float  # USD per month
    latency_target_ms: int
    risk_tolerance: str  # low, medium, high
    compliance_level: str  # low, medium, high
    expected_users: int


class Weights(TypedDict):
    """Optimization weights (must sum to 1.0)."""
    cost: float
    latency: float
    risk: float
    compliance: float
    scalability: float
    complexity: float


class RawMetrics(TypedDict):
    """Raw simulation metrics before normalization."""
    estimated_monthly_cost: float
    p95_latency_ms: int
    risk_score: float  # 0-100
    compliance_score: float  # 0-100
    max_concurrent_users: int
    implementation_complexity: int  # 1-10


class NormalizedScores(TypedDict):
    """Normalized scores (0-100 scale)."""
    cost: float
    latency: float
    risk: float
    compliance: float
    scalability: float
    complexity: float


class SimulationResult(TypedDict):
    """Complete simulation result for an architecture."""
    architecture_id: str
    raw_metrics: RawMetrics
    normalized_scores: NormalizedScores
    final_score: float


class ReflectionFeedback(TypedDict):
    """Reflection agent output."""
    confidence_score: float  # 0.0-1.0
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    should_iterate: bool


class VersionRecord(TypedDict):
    """Single version in iteration history."""
    version: int
    timestamp: str
    architecture_id: str
    architecture: Architecture
    metrics: NormalizedScores
    score: float
    changes_made: List[str]
    parent_version: Optional[int]


class MetaMindState(TypedDict):
    """
    Global state for MetaMind architecture design pipeline.
    
    This state flows through all agents in the LangGraph orchestration.
    """
    
    # Metadata
    run_id: str
    version: int
    timestamp: str
    status: str  # initializing, generating, simulating, optimizing, reflecting, iterating, completed, failed
    
    # Business Requirements
    business_goal: str
    domain: str  # healthcare, finance, ecommerce, education, legal, general
    modalities: List[str]  # text, vision, multimodal, tabular
    
    # Constraints
    constraints: Constraints
    
    # Optimization Weights (domain-adaptive)
    weights: Weights
    
    # Generated Architectures
    candidate_architectures: List[Architecture]
    
    # Simulation Results
    simulation_results: List[SimulationResult]
    
    # Selected Architecture
    selected_architecture: Optional[Architecture]
    selected_architecture_id: Optional[str]
    
    # Reflection & Improvement
    reflection_feedback: Optional[ReflectionFeedback]
    
    # Iteration History
    iteration_history: List[VersionRecord]
    current_iteration: int
    max_iterations: int
    
    # Final Outputs
    technical_specification: Optional[str]
    deployment_plan: Optional[str]
    monitoring_strategy: Optional[str]
    executive_report: Optional[str]
    
    # Error Handling
    errors: List[str]
    warnings: List[str]


def create_initial_state(
    business_goal: str,
    domain: str,
    modalities: List[str],
    constraints: Dict[str, Any],
    max_iterations: int = 5
) -> MetaMindState:
    """
    Create an initial state object for the MetaMind pipeline.
    
    Args:
        business_goal: Clear description of the system's purpose
        domain: Application domain (healthcare, finance, etc.)
        modalities: Data types to handle (text, vision, etc.)
        constraints: System constraints (budget, latency, etc.)
        max_iterations: Maximum number of improvement iterations
        
    Returns:
        MetaMindState: Initialized state object
    """
    run_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + "Z"
    
    return MetaMindState(
        # Metadata
        run_id=run_id,
        version=1,
        timestamp=timestamp,
        status="initializing",
        
        # Business Requirements
        business_goal=business_goal,
        domain=domain,
        modalities=modalities,
        
        # Constraints
        constraints=Constraints(
            budget=constraints.get("budget", 10000.0),
            latency_target_ms=constraints.get("latency_target_ms", 500),
            risk_tolerance=constraints.get("risk_tolerance", "medium"),
            compliance_level=constraints.get("compliance_level", "medium"),
            expected_users=constraints.get("expected_users", 10000)
        ),
        
        # Weights (will be set by DomainWeightTuningAgent)
        weights=Weights(
            cost=0.20,
            latency=0.20,
            risk=0.15,
            compliance=0.15,
            scalability=0.15,
            complexity=0.15
        ),
        
        # Generated Architectures
        candidate_architectures=[],
        
        # Simulation Results
        simulation_results=[],
        
        # Selected Architecture
        selected_architecture=None,
        selected_architecture_id=None,
        
        # Reflection
        reflection_feedback=None,
        
        # Iteration
        iteration_history=[],
        current_iteration=1,
        max_iterations=max_iterations,
        
        # Final Outputs
        technical_specification=None,
        deployment_plan=None,
        monitoring_strategy=None,
        executive_report=None,
        
        # Error Handling
        errors=[],
        warnings=[]
    )


def validate_state(state: MetaMindState) -> tuple[bool, List[str]]:
    """
    Validate that the state has required fields populated correctly.
    
    Args:
        state: The state object to validate
        
    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []
    
    # Check required fields
    if not state.get("run_id"):
        errors.append("Missing run_id")
    
    if not state.get("business_goal"):
        errors.append("Missing business_goal")
    
    if not state.get("domain"):
        errors.append("Missing domain")
    
    if not state.get("modalities") or len(state["modalities"]) == 0:
        errors.append("Missing or empty modalities")
    
    # Validate constraints
    constraints = state.get("constraints", {})
    if constraints.get("budget", 0) <= 0:
        errors.append("Budget must be positive")
    
    if constraints.get("latency_target_ms", 0) <= 0:
        errors.append("Latency target must be positive")
    
    if constraints.get("expected_users", 0) <= 0:
        errors.append("Expected users must be positive")
    
    # Validate weights sum to 1.0
    weights = state.get("weights", {})
    weight_sum = sum([
        weights.get("cost", 0),
        weights.get("latency", 0),
        weights.get("risk", 0),
        weights.get("compliance", 0),
        weights.get("scalability", 0),
        weights.get("complexity", 0)
    ])
    
    if abs(weight_sum - 1.0) > 0.01:
        errors.append(f"Weights must sum to 1.0 (current sum: {weight_sum})")
    
    return len(errors) == 0, errors


def get_state_summary(state: MetaMindState) -> Dict[str, Any]:
    """
    Get a summary of the current state for logging/debugging.
    
    Args:
        state: The state object
        
    Returns:
        Dict: Summary of state with key information
    """
    return {
        "run_id": state.get("run_id"),
        "version": state.get("version"),
        "status": state.get("status"),
        "timestamp": state.get("timestamp"),
        "domain": state.get("domain"),
        "current_iteration": state.get("current_iteration"),
        "max_iterations": state.get("max_iterations"),
        "candidates_generated": len(state.get("candidate_architectures", [])),
        "simulations_completed": len(state.get("simulation_results", [])),
        "selected_architecture": state.get("selected_architecture_id"),
        "reflection_confidence": state.get("reflection_feedback", {}).get("confidence_score"),
        "should_iterate": state.get("reflection_feedback", {}).get("should_iterate"),
        "errors_count": len(state.get("errors", [])),
        "warnings_count": len(state.get("warnings", []))
    }


def add_version_to_history(
    state: MetaMindState,
    architecture: Architecture,
    metrics: NormalizedScores,
    score: float,
    changes_made: List[str]
) -> MetaMindState:
    """
    Add a new version record to the iteration history.
    
    Args:
        state: Current state
        architecture: Architecture for this version
        metrics: Normalized metrics
        score: Final score
        changes_made: List of changes from previous version
        
    Returns:
        MetaMindState: Updated state with new version record
    """
    version_record = VersionRecord(
        version=state["version"],
        timestamp=datetime.utcnow().isoformat() + "Z",
        architecture_id=architecture["architecture_id"],
        architecture=architecture,
        metrics=metrics,
        score=score,
        changes_made=changes_made,
        parent_version=state["version"] - 1 if state["version"] > 1 else None
    )
    
    state["iteration_history"].append(version_record)
    return state


def increment_version(state: MetaMindState) -> MetaMindState:
    """
    Increment the version number and iteration counter.
    
    Args:
        state: Current state
        
    Returns:
        MetaMindState: Updated state with incremented version
    """
    state["version"] += 1
    state["current_iteration"] += 1
    state["timestamp"] = datetime.utcnow().isoformat() + "Z"
    return state


def should_continue_iteration(state: MetaMindState) -> bool:
    """
    Determine if iteration should continue based on reflection feedback.
    
    Args:
        state: Current state
        
    Returns:
        bool: True if should iterate, False otherwise
    """
    # Check if max iterations reached
    if state["current_iteration"] >= state["max_iterations"]:
        state["warnings"].append(f"Max iterations ({state['max_iterations']}) reached")
        return False
    
    # Check reflection feedback
    reflection = state.get("reflection_feedback")
    if not reflection:
        return False
    
    # Check confidence threshold
    confidence = reflection.get("confidence_score", 0.0)
    should_iterate = reflection.get("should_iterate", False)
    
    if confidence >= 0.85:
        return False
    
    if should_iterate and confidence < 0.85:
        return True
    
    return False


# Architecture Templates
ARCHITECTURE_TEMPLATES = [
    "LLM + RAG Pipeline",
    "Multi-Agent LLM System",
    "Vision + LLM Multimodal Pipeline",
    "Tool-Augmented Agent System",
    "Fine-Tuned Compact Model Pipeline",
    "Hybrid Multi-Model Arbitration Pipeline"
]

# Valid domains
VALID_DOMAINS = [
    "healthcare",
    "finance",
    "ecommerce",
    "education",
    "legal",
    "general"
]

# Valid modalities
VALID_MODALITIES = [
    "text",
    "vision",
    "multimodal",
    "tabular"
]

# Pipeline layers
PIPELINE_LAYERS = [
    "Data Layer",
    "Preprocessing Layer",
    "Embedding Layer",
    "Model Layer",
    "Tool Layer",
    "Agent Orchestration Layer",
    "Validation & Safety Layer",
    "Monitoring Layer",
    "Deployment Layer"
]

# Made with Bob
