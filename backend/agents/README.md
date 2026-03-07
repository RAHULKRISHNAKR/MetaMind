# MetaMind Agents Architecture

This directory contains the specialized agents that power MetaMind's autonomous AI pipeline design system. Each agent has a specific responsibility in the multi-agent workflow orchestrated by LangGraph.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MetaMind Agent Workflow                          │
└─────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │   START      │
                              │  (User Input)│
                              └──────┬───────┘
                                     │
                              ┌──────▼───────────────────┐
                              │  RequirementAgent        │
                              │  (LLM-based)             │
                              │  • Parse requirements    │
                              │  • Validate constraints  │
                              │  • Structure input       │
                              └──────┬───────────────────┘
                                     │
                              ┌──────▼───────────────────┐
                              │ DomainWeightTuningAgent  │
                              │ (Rule-based)             │
                              │ • Set optimization       │
                              │   weights by domain      │
                              │ • Healthcare: Risk 30%   │
                              │ • Finance: Latency 25%   │
                              └──────┬───────────────────┘
                                     │
                       ┌─────────────▼──────────────────┐
                       │ ArchitectureGenerationAgent    │
                       │ (LLM-based)                    │
                       │ • Generate 3-5 candidates      │
                       │ • Use predefined templates     │
                       │ • Ensure diversity             │
                       └─────────────┬──────────────────┘
                                     │
                              ┌──────▼───────────────────┐
                              │   SimulationAgent        │
                              │   (Hybrid)               │
                              │   • Estimate cost        │
                              │   • Calculate latency    │
                              │   • Assess risk (LLM)    │
                              │   • Check compliance     │
                              └──────┬───────────────────┘
                                     │
                              ┌──────▼───────────────────┐
                              │ DeterministicScoringEngine│
                              │ (Rule-based)             │
                              │ • Normalize metrics      │
                              │ • Apply domain weights   │
                              │ • Calculate final scores │
                              └──────┬───────────────────┘
                                     │
                              ┌──────▼───────────────────┐
                              │  OptimizationAgent       │
                              │  (Rule-based)            │
                              │  • Select best arch      │
                              │  • Handle ties           │
                              │  • Generate justification│
                              └──────┬───────────────────┘
                                     │
                              ┌──────▼───────────────────┐
                              │   ReflectionAgent        │
                              │   (LLM-based)            │
                              │   • Critique design      │
                              │   • Assess confidence    │
                              │   • Suggest improvements │
                              └──────┬───────────────────┘
                                     │
                         ┌───────────▼────────────┐
                         │  Confidence >= 0.85?   │
                         │  OR Max iterations?    │
                         └───┬────────────────┬───┘
                             │ NO             │ YES
                    ┌────────▼──────┐    ┌───▼────────────────┐
                    │ IterationAgent │    │  VersioningAgent   │
                    │ (Hybrid)       │    │  (Rule-based)      │
                    │ • Apply fixes  │    │  • Store version   │
                    │ • Increment v  │    │  • Update DB       │
                    └────────┬───────┘    └───┬────────────────┘
                             │                │
                             │ Loop back      │
                             │ to Simulation  │
                             └────────────────┤
                                              │
                                       ┌──────▼───────────────┐
                                       │  ComparisonAgent     │
                                       │  (Rule-based)        │
                                       │  • Compare versions  │
                                       │  • Calculate deltas  │
                                       └──────┬───────────────┘
                                              │
                                       ┌──────▼───────────────┐
                                       │ SpecGeneratorAgent   │
                                       │ (LLM-based)          │
                                       │ • Executive summary  │
                                       │ • Tech spec          │
                                       │ • Deployment plan    │
                                       │ • Monitoring strategy│
                                       └──────┬───────────────┘
                                              │
                                       ┌──────▼───────────────┐
                                       │   CodeGeneratorAgent │
                                       │   (Template-based)   │
                                       │   • Generate code    │
                                       │   • Create ZIP       │
                                       └──────┬───────────────┘
                                              │
                                       ┌──────▼───────────────┐
                                       │      END             │
                                       │  (Complete Design)   │
                                       └──────────────────────┘
```

## Agent Types

### 🤖 LLM-Based Agents
Use language models for reasoning, generation, and assessment:
- **RequirementAgent**: Parse natural language into structured constraints
- **ArchitectureGenerationAgent**: Generate diverse architecture candidates
- **ReflectionAgent**: Critique designs and assess confidence
- **SpecGeneratorAgent**: Generate comprehensive documentation

### 📊 Rule-Based Agents
Use deterministic algorithms for consistent, reproducible results:
- **DomainWeightTuningAgent**: Map domains to optimization weights
- **DeterministicScoringEngine**: Normalize metrics and calculate scores
- **OptimizationAgent**: Select optimal architecture
- **VersioningAgent**: Persist architecture versions
- **ComparisonAgent**: Compare architecture versions

### 🔄 Hybrid Agents
Combine rule-based logic with LLM capabilities:
- **SimulationAgent**: Rule-based cost/latency + LLM-based risk/compliance
- **IterationAgent**: Rule-based improvements + LLM guidance

### 🛠️ Utility Agents
Support code generation and deployment:
- **CodeGeneratorAgent**: Template-based code generation

## Detailed Agent Descriptions

### 1. RequirementAgent
**Type**: LLM-based  
**Input**: Natural language requirements  
**Output**: Structured constraints (budget, latency, domain, etc.)  
**LLM Provider**: Groq (configurable via `.env`)

Parses user input and validates against predefined schemas. Handles missing fields by inferring reasonable defaults based on domain.

**Key Features**:
- Domain validation (healthcare, finance, ecommerce, education, legal, general)
- Modality validation (text, vision, multimodal, tabular)
- Constraint normalization
- Pydantic validation

---

### 2. DomainWeightTuningAgent
**Type**: Rule-based  
**Input**: Domain name  
**Output**: Optimization weights (must sum to 1.0)

Maps application domains to optimization priorities:

| Domain | Cost | Latency | Risk | Compliance | Scalability | Complexity |
|--------|------|---------|------|------------|-------------|------------|
| Healthcare | 10% | 15% | **30%** | **30%** | 10% | 5% |
| Finance | 15% | **25%** | **25%** | **25%** | 5% | 5% |
| E-commerce | **25%** | **25%** | 10% | 10% | **20%** | 10% |
| Education | **30%** | 15% | 15% | 15% | 15% | 10% |
| Legal | 10% | 15% | **25%** | **35%** | 10% | 5% |
| General | 20% | 20% | 15% | 15% | 15% | 15% |

---

### 3. ArchitectureGenerationAgent
**Type**: LLM-based  
**Input**: Requirements + weights  
**Output**: 3-5 diverse architecture candidates  
**LLM Provider**: Groq (configurable)

Generates candidate architectures using predefined templates:
- LLM + RAG Pipeline
- Multi-Agent LLM System
- Vision + LLM Multimodal Pipeline
- Tool-Augmented Agent System
- Fine-Tuned Compact Model Pipeline
- Hybrid Multi-Model Arbitration Pipeline

**Validation**:
- Component validation against [`architecture_components.py`](./architecture_components.py)
- Template validation
- Diversity enforcement (max 2 per template)

---

### 4. SimulationAgent
**Type**: Hybrid (Rule-based + LLM)  
**Input**: Architecture candidates  
**Output**: Raw metrics for each candidate  
**LLM Provider**: Groq (for risk/compliance assessment)

**Rule-Based Metrics**:
- **Cost**: Model pricing + infrastructure costs + 20% overhead
- **Latency**: Base latency + model time + DB time + network (adjusted by topology)
- **Scalability**: Base capacity × scaling factors (Kubernetes, Redis, load balancer)
- **Complexity**: Component count + topology + specialized tech

**LLM-Based Metrics**:
- **Risk**: Security, reliability, failure modes, operational risks
- **Compliance**: GDPR, HIPAA, SOC2, audit trails, data protection

---

### 5. DeterministicScoringEngine
**Type**: Rule-based  
**Input**: Raw metrics + weights  
**Output**: Normalized scores (0-100) + final weighted score

**Normalization Curves**:
- **Cost**: 100 if ≤70% budget, linear decay to 0 if >200% budget
- **Latency**: 100 if ≤80% target, linear decay to 0 if >200% target
- **Scalability**: 100 if ≥150% expected users, linear scale below
- **Complexity**: Linear mapping from 1 (100 points) to 10 (0 points)
- **Risk/Compliance**: Already 0-100 from LLM

**Final Score**: Weighted sum using domain-specific weights

---

### 6. OptimizationAgent
**Type**: Rule-based  
**Input**: Scored candidates  
**Output**: Selected architecture + justification

**Selection Logic**:
1. Sort by final score (descending)
2. Handle ties (within 0.5 points) by preferring lower complexity
3. Generate justification based on score advantage and top metrics

---

### 7. ReflectionAgent
**Type**: LLM-based  
**Input**: Selected architecture + metrics  
**Output**: Confidence score + critique + improvement suggestions  
**LLM Provider**: Groq (configurable)

**Confidence Threshold**: 0.85  
**Output Includes**:
- Confidence score (0.0-1.0)
- Strengths (what works well)
- Weaknesses (what needs improvement)
- Specific improvement suggestions
- Should iterate decision
- **NEW**: Detailed score explanations with context

**Score Explanations** (Task 4 - COMPLETED):
Each metric now includes:
- How it's calculated
- What the score means
- Interpretation (Excellent/Good/Poor)
- Use case and importance

---

### 8. IterationAgent
**Type**: Hybrid  
**Input**: Reflection feedback  
**Output**: Improved architecture  
**LLM Provider**: Groq (configurable)

**Improvement Patterns**:
- Add Redis caching (if latency/cost issues)
- Switch to smaller model (if cost issues)
- Optimize topology (sequential → parallel)
- Add load balancing (if scalability issues)
- Enhance monitoring (add Prometheus/Grafana)
- Add validation layers (if risk issues)
- Enhance compliance (audit logging, encryption)

---

### 9. VersioningAgent
**Type**: Rule-based  
**Input**: Architecture version  
**Output**: Database record

Persists architecture versions to SQLite database:
- **runs** table: Run metadata
- **architectures** table: Version history with parent-child links

---

### 10. ComparisonAgent
**Type**: Rule-based  
**Input**: Two architecture versions  
**Output**: Comparison report

Calculates:
- Score delta
- Metric deltas
- Improvements vs regressions
- Recommendation (improvement/regression)

---

### 11. SpecGeneratorAgent
**Type**: LLM-based  
**Input**: Final architecture  
**Output**: Complete documentation  
**LLM Provider**: Groq (configurable)

Generates:
- **Executive Summary**: Non-technical overview for stakeholders
- **Technical Specification**: Detailed component breakdown
- **Deployment Plan**: Step-by-step deployment guide
- **Monitoring Strategy**: KPIs, alerts, dashboards

---

### 12. CodeGeneratorAgent
**Type**: Template-based (Jinja2)  
**Input**: Architecture blueprint  
**Output**: Production-ready code + ZIP archive

**Supported Architectures**:
- ✅ RAG Pipeline (Python)
- ✅ Healthcare Monitoring System (Python)
- ⚠️ Multi-Agent System (TODO - Task 2)
- ⚠️ Fine-Tuned Model (TODO - Task 2)
- ⚠️ Hybrid Architecture (TODO - Task 2)
- ⚠️ Ensemble System (TODO - Task 2)

**Generated Files**:
- `main.py`: Application entry point
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration
- `docker-compose.yml`: Multi-container setup
- `.env`: Environment variables
- `README.md`: Project documentation

---

## LLM Provider Configuration

**Default Provider**: Groq (fast, free tier available)  
**Fallback Chain**: Groq → Ollama → xAI → OpenAI → Anthropic

Configure via `.env`:
```bash
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_BASE_URL=https://api.groq.com/openai/v1
```

**Seamless Switching** (Task 3 - COMPLETED):
All agents now use [`create_llm_from_env()`](../utils/llm_utils.py) for provider-agnostic LLM initialization. No code changes needed to switch providers.

---

## State Management

All agents operate on a shared [`MetaMindState`](../orchestration/state.py) object that flows through the LangGraph pipeline. The state includes:

- **Metadata**: run_id, version, timestamp, status
- **Requirements**: business_goal, domain, modalities
- **Constraints**: budget, latency, users, risk, compliance
- **Weights**: Domain-specific optimization weights
- **Architectures**: Candidates, selected, simulation results
- **Reflection**: Confidence, strengths, weaknesses, suggestions
- **History**: Version records with parent-child links
- **Outputs**: Technical spec, deployment plan, monitoring strategy
- **Errors/Warnings**: Accumulated issues

---

## Error Handling

All agents implement robust error handling:
- **Try-catch blocks**: Capture exceptions without crashing pipeline
- **Error accumulation**: Store errors in `state["errors"]`
- **Warning accumulation**: Store warnings in `state["warnings"]`
- **Fallback mechanisms**: Default values when LLM fails
- **Retry logic**: Built into LLM utilities (exponential backoff)
- **Logging**: Structured logging via [`AgentLogger`](../utils/logging_config.py)

---

## Logging

All agents use [`AgentLogger`](../utils/logging_config.py) for structured logging:

```python
from ..utils.logging_config import AgentLogger

class MyAgent:
    def __init__(self):
        self.logger = AgentLogger("MyAgent")
    
    def execute(self, state):
        self.logger.info("Starting execution")
        # ... agent logic ...
        self.logger.log_execution_success(run_id, duration, details)
```

**Log Levels**:
- `info()`: General execution flow
- `warning()`: Non-critical issues
- `error()`: Failures and exceptions
- `log_execution_start()`: Agent start with metadata
- `log_execution_success()`: Agent completion with metrics
- `log_execution_failure()`: Agent failure with error details
- `log_llm_call()`: LLM invocation with token counts

---

## Testing

Each agent can be tested independently:

```python
from backend.agents import RequirementAgent
from backend.orchestration.state import create_initial_state

# Create test state
state = create_initial_state(
    business_goal="Build a chatbot",
    domain="general",
    modalities=["text"],
    constraints={"budget": 5000, "latency_target_ms": 500}
)

# Test agent
agent = RequirementAgent()
result = agent.execute(state)

print(result["domain"])  # "general"
print(result["constraints"])  # Validated constraints
```

---

## Performance Considerations

- **LLM Calls**: Expensive and slow. Use caching where possible.
- **Retry Logic**: Exponential backoff prevents API rate limits
- **Parallel Execution**: Not currently implemented (sequential pipeline)
- **Database**: SQLite for simplicity; consider PostgreSQL for production
- **Memory**: State object grows with iterations; limit max_iterations

---

## Future Enhancements

1. **Streaming Logs** (Task 1 - IN PROGRESS): Real-time progress updates to frontend
2. **Cost Breakdown** (Task 7 - PENDING): Detailed per-component cost estimates
3. **Template Expansion** (Task 2 - PENDING): Multi-agent, fine-tuned, hybrid, ensemble
4. **Parallel Simulation**: Simulate candidates concurrently
5. **Advanced Caching**: Cache LLM responses for identical inputs
6. **A/B Testing**: Compare multiple architectures in production
7. **Auto-tuning**: Learn optimal weights from historical data

---

## Contributing

When adding new agents:
1. Inherit from base pattern (see existing agents)
2. Implement `execute(state: MetaMindState) -> MetaMindState`
3. Add error handling and logging
4. Update [`__init__.py`](./__init__.py) exports
5. Register in [`graph.py`](../orchestration/graph.py)
6. Add tests
7. Update this README

---

## Related Documentation

- [Orchestration README](../orchestration/README.md) - LangGraph workflow
- [State Schema](../orchestration/state.py) - Shared state definition
- [LLM Utils](../utils/llm_utils.py) - Provider abstraction
- [Validation](../utils/validation.py) - Pydantic schemas
- [API Endpoints](../api/main.py) - REST API

---

**Last Updated**: 2026-03-07  
**Version**: 1.0.0  
**Maintainer**: MetaMind Team