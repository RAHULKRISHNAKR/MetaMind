# MetaMind Orchestration

This directory contains the LangGraph-based orchestration layer that coordinates the multi-agent workflow for autonomous AI pipeline design.

## Overview

The orchestration layer uses [LangGraph](https://github.com/langchain-ai/langgraph) to create a stateful, multi-agent workflow with conditional edges and iteration loops. It manages the flow of the [`MetaMindState`](./state.py) object through all agents in the pipeline.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LangGraph Orchestration Layer                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────┐         ┌──────────────┐        ┌──────────────┐  │
│  │   graph.py  │────────▶│   state.py   │◀───────│   Agents     │  │
│  │             │         │              │        │              │  │
│  │ • Workflow  │         │ • State      │        │ • Execute    │  │
│  │ • Nodes     │         │   Schema     │        │ • Transform  │  │
│  │ • Edges     │         │ • Validation │        │ • Return     │  │
│  │ • Routing   │         │ • Helpers    │        │              │  │
│  └─────────────┘         └──────────────┘        └──────────────┘  │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Files

### [`graph.py`](./graph.py)
Defines the LangGraph workflow and orchestrator class.

**Key Components**:
- `MetaMindOrchestrator`: Main orchestrator class
- `_build_graph()`: Constructs the state graph with nodes and edges
- `_should_iterate()`: Conditional routing logic
- `design()`: Public API for running the pipeline

### [`state.py`](./state.py)
Defines the shared state schema and helper functions.

**Key Components**:
- `MetaMindState`: TypedDict defining the complete state structure
- `create_initial_state()`: Factory function for new runs
- `validate_state()`: State validation logic
- `should_continue_iteration()`: Iteration decision logic
- Helper functions for state manipulation

## Workflow Execution

### Linear Flow (No Iteration)

```
START
  │
  ├─▶ RequirementAgent
  │     │
  │     ├─▶ DomainWeightTuningAgent
  │     │     │
  │     │     ├─▶ ArchitectureGenerationAgent
  │     │     │     │
  │     │     │     ├─▶ SimulationAgent
  │     │     │     │     │
  │     │     │     │     ├─▶ DeterministicScoringEngine
  │     │     │     │     │     │
  │     │     │     │     │     ├─▶ OptimizationAgent
  │     │     │     │     │     │     │
  │     │     │     │     │     │     ├─▶ ReflectionAgent
  │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     ├─▶ [Confidence >= 0.85?]
  │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     └─▶ YES
  │     │     │     │     │     │     │     │           │
  │     │     │     │     │     │     │     │           ├─▶ VersioningAgent
  │     │     │     │     │     │     │     │           │     │
  │     │     │     │     │     │     │     │           │     ├─▶ ComparisonAgent
  │     │     │     │     │     │     │     │           │     │     │
  │     │     │     │     │     │     │     │           │     │     ├─▶ SpecGeneratorAgent
  │     │     │     │     │     │     │     │           │     │     │     │
  │     │     │     │     │     │     │     │           │     │     │     └─▶ END
```

### Iteration Loop (Confidence < 0.85)

```
ReflectionAgent
  │
  ├─▶ [Confidence < 0.85?]
  │     │
  │     └─▶ YES
  │           │
  │           ├─▶ IterationAgent
  │           │     │
  │           │     ├─▶ Increment version
  │           │     │     │
  │           │     │     ├─▶ Apply improvements
  │           │     │     │     │
  │           │     │     │     └─▶ Loop back to SimulationAgent
  │           │     │     │           │
  │           │     │     │           ├─▶ SimulationAgent (re-simulate)
  │           │     │     │           │     │
  │           │     │     │           │     ├─▶ DeterministicScoringEngine (re-score)
  │           │     │     │           │     │     │
  │           │     │     │           │     │     ├─▶ OptimizationAgent (re-select)
  │           │     │     │           │     │     │     │
  │           │     │     │           │     │     │     ├─▶ ReflectionAgent (re-assess)
  │           │     │     │           │     │     │     │     │
  │           │     │     │           │     │     │     │     └─▶ [Check again...]
  │           │     │     │           │     │     │     │
  │           │     │     │           │     │     │     └─▶ (Repeat until confidence >= 0.85
  │           │     │     │           │     │     │          or max_iterations reached)
```

## State Management

### State Flow

The `MetaMindState` object flows through all agents:

```python
state = create_initial_state(
    business_goal="Build a chatbot",
    domain="healthcare",
    modalities=["text"],
    constraints={
        "budget": 5000,
        "latency_target_ms": 500,
        "expected_users": 10000,
        "risk_tolerance": "high",
        "compliance_level": "high"
    },
    max_iterations=5
)

# State flows through pipeline
state = requirement_agent.execute(state)
state = weight_tuning_agent.execute(state)
state = architecture_generation_agent.execute(state)
# ... and so on
```

### State Structure

```python
MetaMindState = {
    # Metadata
    "run_id": str,              # Unique run identifier
    "version": int,             # Current version number
    "timestamp": str,           # ISO 8601 timestamp
    "status": str,              # Current pipeline status
    
    # Requirements
    "business_goal": str,       # User's objective
    "domain": str,              # Application domain
    "modalities": List[str],    # Data types
    
    # Constraints
    "constraints": {
        "budget": float,
        "latency_target_ms": int,
        "expected_users": int,
        "risk_tolerance": str,
        "compliance_level": str
    },
    
    # Optimization
    "weights": {                # Domain-specific weights
        "cost": float,
        "latency": float,
        "risk": float,
        "compliance": float,
        "scalability": float,
        "complexity": float
    },
    
    # Architectures
    "candidate_architectures": List[Architecture],
    "selected_architecture": Architecture,
    "simulation_results": List[SimulationResult],
    
    # Reflection
    "reflection_feedback": {
        "confidence_score": float,
        "strengths": List[str],
        "weaknesses": List[str],
        "improvement_suggestions": List[str],
        "should_iterate": bool
    },
    
    # Iteration
    "iteration_history": List[VersionRecord],
    "current_iteration": int,
    "max_iterations": int,
    
    # Outputs
    "technical_specification": str,
    "deployment_plan": str,
    "monitoring_strategy": str,
    "executive_report": str,
    
    # Error Handling
    "errors": List[str],
    "warnings": List[str]
}
```

## Conditional Routing

### Iteration Decision

The `_should_iterate()` method determines whether to continue iterating:

```python
def _should_iterate(self, state: MetaMindState) -> str:
    """
    Route to either 'iterate' or 'finalize' based on:
    1. Confidence score (must be >= 0.85)
    2. Max iterations (must not exceed limit)
    """
    if state["current_iteration"] >= state["max_iterations"]:
        return "finalize"  # Max iterations reached
    
    reflection = state.get("reflection_feedback")
    if not reflection:
        return "finalize"  # No reflection available
    
    confidence = reflection.get("confidence_score", 0.0)
    should_iterate = reflection.get("should_iterate", False)
    
    if confidence >= 0.85:
        return "finalize"  # Confidence threshold met
    
    if should_iterate and confidence < 0.85:
        return "iterate"   # Need improvement
    
    return "finalize"
```

### Edge Configuration

```python
# Conditional edge from ReflectionAgent
workflow.add_conditional_edges(
    "reflection",
    self._should_iterate,
    {
        "iterate": "iteration",      # Low confidence → improve
        "finalize": "versioning"     # High confidence → finalize
    }
)

# Iteration loop back to simulation
workflow.add_edge("iteration", "simulation")
```

## Node Execution

Each node wraps an agent's `execute()` method:

```python
def _requirement_node(self, state: MetaMindState) -> MetaMindState:
    """Execute RequirementAgent."""
    print(f"[{state['run_id']}] Executing RequirementAgent...")
    state["status"] = "parsing_requirements"
    return self.requirement_agent.execute(state)
```

**Node Responsibilities**:
1. Log execution start
2. Update status
3. Call agent's `execute()` method
4. Return updated state

## Version Management

### Version Increment

```python
def increment_version(state: MetaMindState) -> MetaMindState:
    """Increment version for new iteration."""
    state["version"] += 1
    state["current_iteration"] += 1
    state["timestamp"] = datetime.utcnow().isoformat() + "Z"
    return state
```

### Version History

```python
def add_version_to_history(
    state: MetaMindState,
    architecture: Architecture,
    metrics: NormalizedScores,
    score: float,
    changes_made: List[str]
) -> MetaMindState:
    """Add version record to history."""
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
```

## Error Handling

### Agent-Level Errors

Each agent handles its own errors:

```python
def execute(self, state: MetaMindState) -> MetaMindState:
    try:
        # Agent logic
        result = self._do_work(state)
        return result
    except Exception as e:
        error_msg = f"AgentName failed: {str(e)}"
        state["errors"].append(error_msg)
        # Apply fallback or default behavior
        return state
```

### Pipeline-Level Errors

The orchestrator catches top-level failures:

```python
def design(self, ...):
    try:
        final_state = self.graph.invoke(initial_state)
        final_state["status"] = "completed"
        return final_state
    except Exception as e:
        print(f"Design failed: {str(e)}")
        initial_state["status"] = "failed"
        initial_state["errors"].append(str(e))
        return initial_state
```

## Usage Example

### Basic Usage

```python
from backend.orchestration.graph import create_orchestrator

# Create orchestrator
orchestrator = create_orchestrator(
    ollama_base_url="http://localhost:11434",  # Deprecated
    model_name="llama3",                       # Deprecated
    db_path="./metamind.db"
)

# Run design pipeline
result = orchestrator.design(
    business_goal="Build a patient monitoring system",
    domain="healthcare",
    modalities=["text", "tabular"],
    constraints={
        "budget": 10000,
        "latency_target_ms": 500,
        "expected_users": 5000,
        "risk_tolerance": "high",
        "compliance_level": "high"
    },
    max_iterations=5
)

# Access results
print(f"Run ID: {result['run_id']}")
print(f"Final Version: {result['version']}")
print(f"Selected Architecture: {result['selected_architecture']['name']}")
print(f"Final Score: {result['score']}")
```

### With Progress Callback

```python
def progress_callback(stage: str, message: str):
    print(f"[{stage}] {message}")

result = orchestrator.design(
    business_goal="...",
    domain="healthcare",
    modalities=["text"],
    constraints={...},
    max_iterations=5,
    progress_callback=progress_callback
)
```

## Graph Visualization

Get a text representation of the workflow:

```python
orchestrator = create_orchestrator()
print(orchestrator.get_graph_visualization())
```

Output:
```
MetaMind Architecture Design Pipeline:

    START
      ↓
[RequirementAgent] - Parse and validate requirements
      ↓
[DomainWeightTuningAgent] - Set optimization weights
      ↓
[ArchitectureGenerationAgent] - Generate 3-5 candidates
      ↓
[SimulationAgent] - Estimate metrics
      ↓
[DeterministicScoringEngine] - Normalize and score
      ↓
[OptimizationAgent] - Select best architecture
      ↓
[ReflectionAgent] - Critique and assess confidence
      ↓
   Decision: confidence >= 0.85?
      ├─ NO → [IterationAgent] - Improve architecture
      │         ↓
      │    (loop back to SimulationAgent)
      │
      └─ YES → [VersioningAgent] - Store final version
                ↓
            [ComparisonAgent] - Compare versions
                ↓
            [SpecGeneratorAgent] - Generate documentation
                ↓
               END
```

## Performance Considerations

### Sequential Execution
- Agents execute one at a time (no parallelization)
- Total time = sum of all agent execution times
- LLM calls are the bottleneck (2-10 seconds each)

### State Size
- State grows with each iteration
- Limit `max_iterations` to prevent memory issues
- Consider state pruning for long-running sessions

### Database I/O
- SQLite is fast for single-user scenarios
- Consider PostgreSQL for concurrent access
- Version history can grow large over time

## Configuration

### Environment Variables

```bash
# LLM Provider (Task 3 - COMPLETED)
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Database
DB_PATH=./metamind.db

# Iteration Limits
MAX_ITERATIONS=5
CONFIDENCE_THRESHOLD=0.85
```

### Orchestrator Parameters

```python
orchestrator = create_orchestrator(
    ollama_base_url="http://localhost:11434",  # DEPRECATED (Task 3)
    model_name="llama3",                       # DEPRECATED (Task 3)
    db_path="./metamind.db"                    # Still used
)
```

**Note**: `ollama_base_url` and `model_name` are deprecated. Use environment variables instead (see Task 3).

## Testing

### Unit Testing Nodes

```python
from backend.orchestration.graph import MetaMindOrchestrator
from backend.orchestration.state import create_initial_state

orchestrator = MetaMindOrchestrator()
state = create_initial_state(...)

# Test individual node
result = orchestrator._requirement_node(state)
assert result["domain"] in ["healthcare", "finance", ...]
```

### Integration Testing

```python
def test_full_pipeline():
    orchestrator = create_orchestrator()
    result = orchestrator.design(
        business_goal="Test chatbot",
        domain="general",
        modalities=["text"],
        constraints={"budget": 5000, ...},
        max_iterations=2
    )
    assert result["status"] == "completed"
    assert result["selected_architecture"] is not None
```

## Debugging

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

orchestrator = create_orchestrator()
result = orchestrator.design(...)
```

### Inspect State at Each Step

```python
def debug_callback(stage: str, message: str):
    print(f"[DEBUG] {stage}: {message}")

result = orchestrator.design(
    ...,
    progress_callback=debug_callback
)
```

### Check Error Accumulation

```python
result = orchestrator.design(...)
if result["errors"]:
    print("Errors encountered:")
    for error in result["errors"]:
        print(f"  - {error}")
```

## Future Enhancements

1. **Parallel Simulation** (PENDING): Simulate candidates concurrently
2. **Streaming Logs** (Task 1 - PENDING): Real-time progress updates to frontend
3. **Checkpointing**: Save/resume pipeline state
4. **Dynamic Routing**: More sophisticated conditional logic
5. **Agent Retries**: Automatic retry on transient failures
6. **State Compression**: Reduce memory footprint for long iterations
7. **Distributed Execution**: Run agents on separate workers

## Related Documentation

- [Agents README](../agents/README.md) - Individual agent documentation
- [State Schema](./state.py) - Complete state definition
- [LLM Utils](../utils/llm_utils.py) - LLM provider abstraction
- [API Endpoints](../api/main.py) - REST API integration

## Troubleshooting

### Issue: Pipeline hangs during LLM calls
**Solution**: Check LLM provider configuration and API keys. Increase timeout values.

### Issue: Max iterations reached without convergence
**Solution**: Lower confidence threshold or increase max_iterations. Review reflection feedback.

### Issue: State validation errors
**Solution**: Check constraint values (budget, latency, users must be positive). Verify weights sum to 1.0.

### Issue: Database locked errors
**Solution**: Ensure only one orchestrator instance per database. Use connection pooling for concurrent access.

---

**Last Updated**: 2026-03-07  
**Version**: 1.0.0  
**Maintainer**: MetaMind Team