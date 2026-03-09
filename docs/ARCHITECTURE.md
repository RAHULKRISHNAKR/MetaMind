# 🏗️ MetaMind Architecture

This document provides a comprehensive overview of MetaMind's system architecture, agent specifications, and design principles.

---

## 📊 System Overview

MetaMind is a **multi-agent AI system** that autonomously designs, optimizes, and iteratively improves AI pipelines. It combines:

- **LLM-based agents** for creative tasks (generation, reflection, documentation)
- **Rule-based agents** for deterministic tasks (scoring, selection, versioning)
- **LangGraph orchestration** for state management and workflow control

---

## 🔄 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                            │
│  Business Goal + Domain + Constraints + Modalities       │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              METAMIND ORCHESTRATOR                       │
│         (LangGraph Multi-Agent Pipeline)                 │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  1. RequirementAgent                              │  │
│  │     Parse & validate requirements                 │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │  2. DomainWeightTuningAgent                      │  │
│  │     Set optimization weights                     │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │  3. ArchitectureGenerationAgent (LLM)            │  │
│  │     Generate 3-5 candidate architectures         │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │  4. SimulationAgent (LLM)                        │  │
│  │     Estimate metrics for each candidate          │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │  5. DeterministicScoringEngine                   │  │
│  │     Normalize & score (NO LLM - pure math)       │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │  6. OptimizationAgent                            │  │
│  │     Select best architecture                     │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                    │
│  ┌──────────────────▼───────────────────────────────┐  │
│  │  7. ReflectionAgent (LLM)                        │  │
│  │     Critique design, assess confidence           │  │
│  └──────────────────┬───────────────────────────────┘  │
│                     │                                    │
│              ┌──────▼──────┐                            │
│              │ Confidence  │                            │
│              │  >= 0.85?   │                            │
│              └──┬──────┬───┘                            │
│                 │ NO   │ YES                            │
│  ┌──────────────▼──┐   │                                │
│  │ 8. IterationAgent│   │                                │
│  │    Improve design│   │                                │
│  └──────────────┬───┘   │                                │
│                 │        │                                │
│         (loop back)      │                                │
│                          │                                │
│  ┌───────────────────────▼────────────────────────────┐ │
│  │  9. VersioningAgent                                │ │
│  │     Store final version in database                │ │
│  └───────────────────┬────────────────────────────────┘ │
│                      │                                    │
│  ┌───────────────────▼────────────────────────────────┐ │
│  │  10. ComparisonAgent                               │ │
│  │      Compare versions (if multiple iterations)     │ │
│  └───────────────────┬────────────────────────────────┘ │
│                      │                                    │
│  ┌───────────────────▼────────────────────────────────┐ │
│  │  11. SpecGeneratorAgent (LLM)                      │ │
│  │      Generate documentation                        │ │
│  └───────────────────┬────────────────────────────────┘ │
│                      │                                    │
└──────────────────────┼────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                    OUTPUT                                │
│  - Optimal Architecture Blueprint                       │
│  - Performance Metrics (6 dimensions)                   │
│  - Overall Score (0-100)                                │
│  - Comprehensive Documentation                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🤖 Agent Specifications

### 1. RequirementAgent (Rule-based)

**Purpose**: Parse and validate user requirements

**Input**: Natural language description
**Output**: Structured constraint schema

**Validation Rules**:
- Domain must be in: healthcare, finance, ecommerce, education, legal, general
- Modalities must be in: text, vision, multimodal, tabular
- Budget must be > 0
- Latency target must be > 0
- Expected users must be > 0

**Output Schema**:
```json
{
  "business_goal": "string",
  "domain": "string",
  "modalities": ["string"],
  "constraints": {
    "budget": "number",
    "latency_target_ms": "number",
    "expected_users": "number",
    "risk_tolerance": "low|medium|high",
    "compliance_level": "low|medium|high"
  }
}
```

---

### 2. DomainWeightTuningAgent (Rule-based)

**Purpose**: Set optimization weights based on domain

**Input**: Domain string
**Output**: Optimization weights (sum to 1.0)

**Domain-Specific Weights**:

| Domain | Cost | Latency | Risk | Compliance | Scalability | Complexity |
|--------|------|---------|------|------------|-------------|------------|
| **Healthcare** | 15% | 20% | 25% | 30% | 5% | 5% |
| **Finance** | 20% | 30% | 20% | 20% | 5% | 5% |
| **E-commerce** | 25% | 25% | 10% | 10% | 20% | 10% |
| **Education** | 30% | 15% | 10% | 15% | 20% | 10% |
| **Legal** | 15% | 20% | 20% | 35% | 5% | 5% |
| **General** | 20% | 20% | 15% | 15% | 20% | 10% |

---

### 3. ArchitectureGenerationAgent (LLM-based)

**Purpose**: Generate diverse architecture candidates

**Input**: Requirements + Weights
**Output**: 3-5 candidate architectures

**Available Templates**:
1. **LLM + RAG Pipeline** - Retrieval-Augmented Generation
2. **Multi-Agent LLM System** - Specialized agents for different tasks
3. **Fine-Tuned Compact Model** - Custom-trained smaller model
4. **Hybrid RAG + Fine-Tuning** - Best of both worlds
5. **Ensemble Multi-Model** - Multiple models voting

**Architecture Components**:
- Data Layer (PostgreSQL, MongoDB, S3, Redis, Kafka)
- Preprocessing Layer (validation, cleaning, feature engineering)
- Embedding Layer (Sentence Transformers, OpenAI, CLIP)
- Model Layer (Llama 3, GPT-4, Claude, Gemini)
- Tool Layer (web search, code execution, database query)
- Agent Orchestration (LangGraph, CrewAI, AutoGen)
- Validation & Safety (input sanitization, output validation)
- Monitoring (logging, metrics, tracing, alerting)
- Deployment (Docker, Kubernetes, API Gateway)

---

### 4. SimulationAgent (Hybrid: Rule-based + LLM)

**Purpose**: Estimate performance metrics for each architecture

**Input**: Architecture specification
**Output**: Raw metrics

**Metrics Estimated**:
```json
{
  "estimated_monthly_cost": "number (USD)",
  "p95_latency_ms": "number (milliseconds)",
  "risk_score": "number (0-100, lower is better)",
  "compliance_score": "number (0-100, higher is better)",
  "max_concurrent_users": "number",
  "implementation_complexity": "number (1-10, lower is better)"
}
```

**Estimation Methods**:
- **Cost**: Rule-based calculation using component pricing
- **Latency**: Rule-based estimation based on topology
- **Risk**: LLM-based assessment
- **Compliance**: Hybrid (rules + LLM)
- **Scalability**: Rule-based capacity calculation
- **Complexity**: Rule-based component counting

---

### 5. DeterministicScoringEngine (Rule-based)

**Purpose**: Normalize metrics and calculate final score

**Input**: Raw metrics + Weights
**Output**: Normalized scores (0-100) + Final score

**Normalization Formulas**:

```python
# Cost Score (higher is better = lower cost)
cost_score = 100 * (1 - (actual_cost / max_budget))

# Latency Score (higher is better = lower latency)
latency_score = 100 * (1 - (actual_latency / target_latency))

# Risk Score (invert so higher is better)
risk_score = 100 - raw_risk_score

# Compliance Score (already 0-100, higher is better)
compliance_score = raw_compliance_score

# Scalability Score (higher is better = more users)
scalability_score = 100 * (actual_users / expected_users)

# Complexity Score (higher is better = lower complexity)
complexity_score = 100 * (1 - (complexity / 10))
```

**Final Score Calculation**:
```python
final_score = (
    weights["cost"] * cost_score +
    weights["latency"] * latency_score +
    weights["risk"] * risk_score +
    weights["compliance"] * compliance_score +
    weights["scalability"] * scalability_score +
    weights["complexity"] * complexity_score
)
```

---

### 6. OptimizationAgent (Rule-based)

**Purpose**: Select the best architecture

**Input**: Scored architectures
**Output**: Selected architecture + Justification

**Selection Logic**:
1. Sort by final score (descending)
2. Select highest scoring architecture
3. Tie-breaking: prefer lower complexity
4. Generate selection justification

---

### 7. ReflectionAgent (LLM-based)

**Purpose**: Critique the selected architecture

**Input**: Selected architecture + Metrics
**Output**: Critique + Confidence score + Improvement suggestions

**Output Schema**:
```json
{
  "confidence_score": "number (0.0-1.0)",
  "strengths": ["string"],
  "weaknesses": ["string"],
  "improvement_suggestions": ["string"],
  "should_iterate": "boolean (confidence < 0.85)"
}
```

**Confidence Threshold**: 0.85
- If confidence >= 0.85: Finalize design
- If confidence < 0.85: Iterate and improve

---

### 8. IterationAgent (Rule-based)

**Purpose**: Apply improvements to architecture

**Input**: Architecture + Reflection feedback
**Output**: Improved architecture (new version)

**Improvement Rules**:
- "caching" → Add Redis caching layer
- "latency" → Switch to smaller/faster model
- "monitoring" → Add comprehensive monitoring
- "load balancing" → Add Nginx load balancer
- "error handling" → Add retry logic and circuit breakers

---

### 9. VersioningAgent (Rule-based)

**Purpose**: Store architecture versions in database

**Input**: Architecture + Metadata
**Output**: Stored version record

**Database Schema**:
```sql
CREATE TABLE runs (
    id TEXT PRIMARY KEY,
    timestamp TEXT,
    business_goal TEXT,
    domain TEXT,
    constraints_json TEXT,
    weights_json TEXT,
    status TEXT
);

CREATE TABLE architectures (
    id TEXT PRIMARY KEY,
    run_id TEXT,
    version INTEGER,
    architecture_json TEXT,
    metrics_json TEXT,
    score REAL,
    changes_made TEXT,
    parent_version INTEGER,
    FOREIGN KEY (run_id) REFERENCES runs(id)
);
```

---

### 10. ComparisonAgent (Rule-based)

**Purpose**: Compare architecture versions

**Input**: Two architecture versions
**Output**: Delta analysis

**Comparison Metrics**:
- Score delta
- Metric deltas (cost, latency, risk, etc.)
- Changes made
- Recommendation (which version is better)

---

### 11. SpecGeneratorAgent (LLM-based)

**Purpose**: Generate comprehensive documentation

**Input**: Final architecture + All metadata
**Output**: 4 comprehensive documents

**Documents Generated**:
1. **Executive Summary** - Business context and key benefits
2. **Technical Specification** - Detailed component breakdown
3. **Deployment Plan** - Step-by-step implementation guide
4. **Monitoring Strategy** - Metrics to track and alerting rules

---

## 🎯 Design Principles

### 1. Hybrid Architecture
- **LLM Agents**: Creative tasks (generation, reflection, documentation)
- **Rule-based Agents**: Deterministic tasks (scoring, selection, versioning)
- **Why**: Combines creativity with reliability

### 2. Deterministic Scoring
- **NO LLM** in scoring engine
- Pure mathematical formulas
- Reproducible results
- No hallucinations

### 3. Iterative Improvement
- Self-reflection loop
- Confidence-based iteration
- Version tracking
- Continuous optimization

### 4. Domain Adaptation
- Domain-specific weight tuning
- Template-based generation
- Constraint enforcement

### 5. Architectural Boundaries
- Predefined component catalog
- No hallucinated technologies
- Validated module structure

---

## 🔧 Technology Stack

### Backend
- **FastAPI** - REST API server
- **LangGraph** - Multi-agent orchestration
- **LangChain** - LLM integration
- **Groq** - Fast LLM inference
- **SQLite** - Version storage
- **Pydantic** - Data validation

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **TypeScript** - Type safety
- **Monaco Editor** - Code editor
- **Tailwind CSS** - Styling

### Infrastructure
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **Nginx** - Web server / Load balancer

---

## 📊 Performance Characteristics

- **Design Time**: 2-5 minutes (with Groq API)
- **Iterations**: 1-5 (typically 2-3)
- **Architectures Generated**: 3-5 per iteration
- **Metrics Tracked**: 6 dimensions
- **Documents Generated**: 4 comprehensive specs
- **Database**: Persistent version history

---

## 🔐 Security Considerations

1. **API Key Management**: Stored in environment variables, never in code
2. **Input Validation**: All user inputs validated with Pydantic
3. **SQL Injection Prevention**: Parameterized queries
4. **CORS Configuration**: Configurable allowed origins
5. **Rate Limiting**: Planned for production deployment

---

## 📈 Scalability

### Horizontal Scaling
- Backend: Multiple replicas behind load balancer
- Frontend: Static assets served via CDN
- Database: Read replicas for query scaling

### Vertical Scaling
- Increase CPU/memory for LLM inference
- Optimize database queries
- Cache frequently accessed data

---

## 🔮 Future Enhancements

1. **Multi-Cloud Support** - AWS, Azure, GCP deployment options
2. **Cost Estimation API** - Real-time pricing from cloud providers
3. **Performance Benchmarking** - Actual load testing integration
4. **A/B Testing** - Deploy multiple versions and compare
5. **Auto-Deployment** - One-click infrastructure provisioning
6. **Custom Templates** - User-defined architecture patterns

---

**MetaMind** - Autonomous AI Pipeline Design at Scale