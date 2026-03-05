# 🔧 MetaMind Implementation Guide

**Complete Technical Documentation for Developers**

This document provides comprehensive implementation details, architecture specifications, and development guidelines for MetaMind.

---

## 📋 Table of Contents

1. [System Architecture](#system-architecture)
2. [Agent Implementation](#agent-implementation)
3. [LangGraph Orchestration](#langgraph-orchestration)
4. [Scoring Engine](#scoring-engine)
5. [API Endpoints](#api-endpoints)
6. [Database Schema](#database-schema)
7. [Frontend Architecture](#frontend-architecture)
8. [Code Generation System](#code-generation-system)
9. [Deployment Guide](#deployment-guide)
10. [Development Workflow](#development-workflow)
11. [Testing Strategy](#testing-strategy)
12. [Performance Optimization](#performance-optimization)

---

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌──────────────────┐              ┌──────────────────┐    │
│  │  Streamlit UI    │              │   React UI       │    │
│  │  (Legacy)        │              │   (Modern)       │    │
│  │  Port: 8501      │              │   Port: 5173     │    │
│  └────────┬─────────┘              └────────┬─────────┘    │
└───────────┼──────────────────────────────────┼──────────────┘
            │                                  │
            └──────────────┬───────────────────┘
                           │ REST API
┌──────────────────────────┼───────────────────────────────────┐
│                    APPLICATION LAYER                          │
│                  ┌───────▼────────┐                          │
│                  │  FastAPI       │                          │
│                  │  Port: 8000    │                          │
│                  │  10 Endpoints  │                          │
│                  └───────┬────────┘                          │
└──────────────────────────┼───────────────────────────────────┘
                           │
┌──────────────────────────┼───────────────────────────────────┐
│                    ORCHESTRATION LAYER                        │
│                  ┌───────▼────────┐                          │
│                  │  LangGraph     │                          │
│                  │  State Machine │                          │
│                  └───────┬────────┘                          │
│                          │                                    │
│    ┌─────────────────────┼─────────────────────┐            │
│    │                     │                     │            │
│    ▼                     ▼                     ▼            │
│ ┌──────┐           ┌──────────┐         ┌──────────┐       │
│ │Agent1│           │  Agent2  │   ...   │  Agent11 │       │
│ └──────┘           └──────────┘         └──────────┘       │
└───────────────────────────────────────────────────────────────┘
            │                     │
            ▼                     ▼
┌─────────────────────┐  ┌─────────────────────┐
│   LLM PROVIDER      │  │   DATA LAYER        │
│   (Grok/Ollama)     │  │   SQLite Database   │
│   API Calls         │  │   Version Storage   │
└─────────────────────┘  └─────────────────────┘
```

### Technology Stack

**Backend:**
- FastAPI 0.115.0 - REST API framework
- LangChain 0.3.0 - LLM orchestration
- LangGraph 0.2.0 - Agent workflow management
- SQLAlchemy 2.0.0 - ORM and database
- Pydantic 2.0.0 - Data validation
- Python 3.11+ - Runtime

**Frontend:**
- React 18.3.1 - Modern UI framework
- Vite 5.4.2 - Build tool
- TailwindCSS 3.4.1 - Styling
- Monaco Editor - Code editor
- Recharts - Data visualization
- Streamlit 1.40.0 - Legacy UI (optional)

**Infrastructure:**
- Docker & Docker Compose - Containerization
- SQLite - Development database
- PostgreSQL - Production database (optional)
- Redis - Caching (optional)

---

## 🤖 Agent Implementation

### 1. RequirementAgent

**Purpose:** Parse natural language requirements into structured JSON

**Input:**
```python
{
    "business_goal": str,
    "domain": str,
    "modalities": List[str],
    "constraints": {
        "budget": float,
        "latency_target_ms": int,
        "expected_users": int,
        "risk_tolerance": str,
        "compliance_level": str
    }
}
```

**Output:**
```python
{
    "parsed_requirements": {
        "goal": str,
        "domain": str,
        "modalities": List[str],
        "constraints": dict
    }
}
```

**Implementation:** [`backend/agents/requirement_agent.py`](backend/agents/requirement_agent.py)

**Key Features:**
- LLM-based natural language understanding
- Structured output with Pydantic validation
- Constraint normalization
- Error handling for invalid inputs

---

### 2. DomainWeightTuningAgent

**Purpose:** Map domain to optimization weights

**Domain Weights:**
```python
DOMAIN_WEIGHTS = {
    "healthcare": {
        "cost": 0.10,
        "latency": 0.15,
        "risk": 0.30,        # High priority
        "compliance": 0.30,   # High priority
        "scalability": 0.10,
        "complexity": 0.05
    },
    "finance": {
        "cost": 0.15,
        "latency": 0.20,
        "risk": 0.25,
        "compliance": 0.25,
        "scalability": 0.10,
        "complexity": 0.05
    },
    "ecommerce": {
        "cost": 0.20,
        "latency": 0.25,     # High priority
        "risk": 0.10,
        "compliance": 0.10,
        "scalability": 0.25,  # High priority
        "complexity": 0.10
    }
}
```

**Implementation:** [`backend/agents/domain_weight_tuning_agent.py`](backend/agents/domain_weight_tuning_agent.py)

---

### 3. ArchitectureGenerationAgent

**Purpose:** Generate 3-5 architecture candidates from templates

**Templates:**
1. **LLM + RAG Pipeline** - Retrieval-augmented generation
2. **Multi-Agent LLM System** - Collaborative AI agents
3. **Vision + LLM Multimodal** - Image and text processing
4. **Tool-Augmented Agent** - External tool integration
5. **Fine-Tuned Compact Model** - Optimized small models
6. **Hybrid Multi-Model** - Multiple model arbitration

**Output Schema:**
```python
{
    "candidates": [
        {
            "name": str,
            "template": str,
            "components": List[str],
            "estimated_cost": float,
            "estimated_latency_ms": int,
            "risk_level": str,
            "compliance_score": float,
            "scalability_rating": str,
            "complexity_score": float
        }
    ]
}
```

**Implementation:** [`backend/agents/architecture_generation_agent.py`](backend/agents/architecture_generation_agent.py)

---

### 4. SimulationAgent

**Purpose:** Estimate 6 metrics for each candidate

**Metrics Calculated:**
- **Cost Score** (0-100): Infrastructure + operational costs
- **Latency Score** (0-100): Response time performance
- **Risk Score** (0-100): Security and reliability risks
- **Compliance Score** (0-100): Regulatory adherence
- **Scalability Score** (0-100): Growth capacity
- **Complexity Score** (0-100): Implementation difficulty

**Implementation:** [`backend/agents/simulation_agent.py`](backend/agents/simulation_agent.py)

---

### 5. DeterministicScoringEngine

**Purpose:** Normalize metrics and compute weighted scores

**Formula:**
```python
final_score = Σ(normalized_metric_i × weight_i)

where:
- normalized_metric_i ∈ [0, 100]
- weight_i ∈ [0, 1]
- Σ(weight_i) = 1.0
```

**Normalization:**
```python
def normalize_cost(cost: float, budget: float) -> float:
    """Lower cost = higher score"""
    if cost <= budget * 0.5:
        return 100.0
    elif cost <= budget:
        return 100.0 - ((cost - budget * 0.5) / (budget * 0.5)) * 50.0
    else:
        return max(0.0, 50.0 - ((cost - budget) / budget) * 50.0)

def normalize_latency(latency: int, target: int) -> float:
    """Lower latency = higher score"""
    if latency <= target:
        return 100.0
    else:
        return max(0.0, 100.0 - ((latency - target) / target) * 100.0)
```

**Implementation:** [`backend/agents/scoring_engine.py`](backend/agents/scoring_engine.py)

---

### 6. OptimizationAgent

**Purpose:** Select highest scoring architecture

**Selection Logic:**
```python
best_candidate = max(candidates, key=lambda c: c["final_score"])
```

**Implementation:** [`backend/agents/optimization_agent.py`](backend/agents/optimization_agent.py)

---

### 7. ReflectionAgent

**Purpose:** Critique design with confidence scoring

**Output:**
```python
{
    "reflection": {
        "strengths": List[str],
        "weaknesses": List[str],
        "improvement_suggestions": List[str],
        "confidence_score": float  # 0.0 - 1.0
    }
}
```

**Confidence Thresholds:**
- `>= 0.85`: Design accepted, no iteration
- `< 0.85`: Trigger iteration for improvement

**Implementation:** [`backend/agents/reflection_agent.py`](backend/agents/reflection_agent.py)

---

### 8. IterationAgent

**Purpose:** Apply improvements based on reflection

**Iteration Logic:**
```python
if confidence_score < 0.85 and iteration_count < max_iterations:
    # Apply improvements
    # Re-generate architecture
    # Re-simulate and score
    # Increment version
else:
    # Finalize design
```

**Implementation:** [`backend/agents/iteration_agent.py`](backend/agents/iteration_agent.py)

---

### 9. VersioningAgent

**Purpose:** Store versions in database

**Version Schema:**
```python
{
    "run_id": str,
    "version": int,
    "architecture_blueprint": dict,
    "scores": dict,
    "weights": dict,
    "reflection_summary": str,
    "timestamp": datetime
}
```

**Implementation:** [`backend/agents/versioning_agent.py`](backend/agents/versioning_agent.py)

---

### 10. ComparisonAgent

**Purpose:** Calculate version deltas

**Delta Calculation:**
```python
delta = {
    "cost_delta": v2.cost - v1.cost,
    "latency_delta": v2.latency - v1.latency,
    "score_delta": v2.final_score - v1.final_score,
    "improvements": List[str],
    "regressions": List[str]
}
```

**Implementation:** [`backend/agents/comparison_agent.py`](backend/agents/comparison_agent.py)

---

### 11. SpecGeneratorAgent

**Purpose:** Generate comprehensive documentation

**Output Sections:**
1. Executive Summary
2. Technical Specification
3. Deployment Plan
4. Monitoring Strategy

**Implementation:** [`backend/agents/spec_generator_agent.py`](backend/agents/spec_generator_agent.py)

---

## 🔄 LangGraph Orchestration

### State Definition

```python
class MetaMindState(TypedDict):
    # Input
    business_goal: str
    domain: str
    modalities: List[str]
    constraints: dict
    max_iterations: int
    
    # Processing
    parsed_requirements: dict
    weights: dict
    candidates: List[dict]
    simulated_candidates: List[dict]
    best_architecture: dict
    reflection: dict
    iteration_count: int
    
    # Output
    final_architecture: dict
    versions: List[dict]
    comparison: dict
    specification: str
```

### Graph Flow

```python
graph = StateGraph(MetaMindState)

# Add nodes
graph.add_node("requirement", requirement_agent)
graph.add_node("domain_weight", domain_weight_agent)
graph.add_node("architecture_gen", architecture_gen_agent)
graph.add_node("simulation", simulation_agent)
graph.add_node("scoring", scoring_engine)
graph.add_node("optimization", optimization_agent)
graph.add_node("reflection", reflection_agent)
graph.add_node("iteration", iteration_agent)
graph.add_node("versioning", versioning_agent)
graph.add_node("comparison", comparison_agent)
graph.add_node("spec_gen", spec_gen_agent)

# Add edges
graph.add_edge("requirement", "domain_weight")
graph.add_edge("domain_weight", "architecture_gen")
graph.add_edge("architecture_gen", "simulation")
graph.add_edge("simulation", "scoring")
graph.add_edge("scoring", "optimization")
graph.add_edge("optimization", "reflection")

# Conditional routing
graph.add_conditional_edges(
    "reflection",
    should_iterate,
    {
        "iterate": "iteration",
        "finalize": "versioning"
    }
)

graph.add_edge("iteration", "architecture_gen")
graph.add_edge("versioning", "comparison")
graph.add_edge("comparison", "spec_gen")
graph.add_edge("spec_gen", END)
```

**Implementation:** [`backend/orchestration/graph.py`](backend/orchestration/graph.py)

---

## 📊 Scoring Engine

### Metric Normalization

All metrics normalized to 0-100 scale where **higher is better**.

**Cost Normalization:**
```python
def normalize_cost(cost: float, budget: float) -> float:
    if cost <= budget * 0.5:
        return 100.0  # Excellent
    elif cost <= budget:
        ratio = (cost - budget * 0.5) / (budget * 0.5)
        return 100.0 - (ratio * 50.0)  # Good to Fair
    else:
        over_budget = (cost - budget) / budget
        return max(0.0, 50.0 - (over_budget * 50.0))  # Poor
```

**Latency Normalization:**
```python
def normalize_latency(latency: int, target: int) -> float:
    if latency <= target:
        return 100.0  # Meets target
    else:
        over_target = (latency - target) / target
        return max(0.0, 100.0 - (over_target * 100.0))  # Penalty
```

**Risk Normalization:**
```python
RISK_MAPPING = {
    "low": 100.0,
    "medium": 60.0,
    "high": 20.0
}
```

**Compliance Normalization:**
```python
COMPLIANCE_MAPPING = {
    "high": 100.0,
    "medium": 60.0,
    "low": 20.0
}
```

**Scalability Normalization:**
```python
SCALABILITY_MAPPING = {
    "excellent": 100.0,
    "good": 75.0,
    "fair": 50.0,
    "poor": 25.0
}
```

**Complexity Normalization:**
```python
def normalize_complexity(complexity: float) -> float:
    # Lower complexity = higher score
    return max(0.0, 100.0 - complexity)
```

### Weighted Score Calculation

```python
def calculate_final_score(
    metrics: dict,
    weights: dict
) -> float:
    score = (
        metrics["cost_score"] * weights["cost"] +
        metrics["latency_score"] * weights["latency"] +
        metrics["risk_score"] * weights["risk"] +
        metrics["compliance_score"] * weights["compliance"] +
        metrics["scalability_score"] * weights["scalability"] +
        metrics["complexity_score"] * weights["complexity"]
    )
    return round(score, 2)
```

---

## 🌐 API Endpoints

### 1. Design Architecture
```http
POST /api/design
Content-Type: application/json

{
  "business_goal": "Build a customer support chatbot",
  "domain": "ecommerce",
  "modalities": ["text"],
  "constraints": {
    "budget": 5000,
    "latency_target_ms": 300,
    "expected_users": 50000,
    "risk_tolerance": "medium",
    "compliance_level": "high"
  },
  "max_iterations": 3
}

Response: 202 Accepted
{
  "run_id": "uuid",
  "status": "processing"
}
```

### 2. Get Design Status
```http
GET /api/design/{run_id}/status

Response: 200 OK
{
  "run_id": "uuid",
  "status": "completed",
  "current_step": "spec_generation",
  "progress": 100
}
```

### 3. Get Design Result
```http
GET /api/design/{run_id}/result

Response: 200 OK
{
  "run_id": "uuid",
  "final_architecture": {...},
  "scores": {...},
  "specification": "...",
  "versions": [...]
}
```

### 4. List Designs
```http
GET /api/designs?limit=10&offset=0

Response: 200 OK
{
  "designs": [...],
  "total": 42
}
```

### 5. Compare Versions
```http
POST /api/compare
Content-Type: application/json

{
  "version1_id": "uuid1",
  "version2_id": "uuid2"
}

Response: 200 OK
{
  "comparison": {...},
  "deltas": {...}
}
```

### 6. Generate Code
```http
POST /api/generate-code
Content-Type: application/json

{
  "run_id": "uuid",
  "language": "python",
  "framework": "fastapi"
}

Response: 200 OK
{
  "files": [
    {
      "path": "main.py",
      "content": "...",
      "language": "python"
    }
  ]
}
```

### 7. Demo Scenarios
```http
GET /api/demo/scenarios

Response: 200 OK
{
  "scenarios": [
    {
      "id": "healthcare",
      "name": "Healthcare Patient Monitoring",
      "description": "..."
    }
  ]
}
```

### 8. Get Demo Result
```http
GET /api/demo/{scenario_id}

Response: 200 OK
{
  "run_id": "demo-healthcare",
  "final_architecture": {...},
  "scores": {...}
}
```

### 9. Health Check
```http
GET /health

Response: 200 OK
{
  "status": "healthy",
  "version": "1.0.0",
  "llm_available": true
}
```

### 10. Metrics
```http
GET /metrics

Response: 200 OK
{
  "total_designs": 42,
  "avg_score": 78.5,
  "avg_iterations": 1.8
}
```

**Implementation:** [`backend/api/main.py`](backend/api/main.py)

---

## 💾 Database Schema

### Designs Table
```sql
CREATE TABLE designs (
    id TEXT PRIMARY KEY,
    business_goal TEXT NOT NULL,
    domain TEXT NOT NULL,
    modalities TEXT NOT NULL,  -- JSON array
    constraints TEXT NOT NULL,  -- JSON object
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Versions Table
```sql
CREATE TABLE versions (
    id TEXT PRIMARY KEY,
    run_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    architecture_blueprint TEXT NOT NULL,  -- JSON
    scores TEXT NOT NULL,  -- JSON
    weights TEXT NOT NULL,  -- JSON
    reflection_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES designs(id)
);
```

### Indexes
```sql
CREATE INDEX idx_designs_status ON designs(status);
CREATE INDEX idx_designs_created_at ON designs(created_at);
CREATE INDEX idx_versions_run_id ON versions(run_id);
CREATE INDEX idx_versions_version ON versions(version);
```

---

## 🎨 Frontend Architecture

### React Application Structure

```
frontend-react/
├── src/
│   ├── components/
│   │   ├── ui/           # Reusable UI components
│   │   ├── layout/       # Layout components
│   │   └── features/     # Feature-specific components
│   ├── pages/
│   │   ├── Design.jsx    # Main design page
│   │   ├── Results.jsx   # Results display
│   │   ├── Editor.jsx    # Code editor
│   │   └── History.jsx   # Design history
│   ├── services/
│   │   └── api.js        # API client
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Utility functions
│   └── App.jsx           # Root component
├── public/
└── package.json
```

### Key Components

**Design Form:**
```jsx
<DesignForm
  onSubmit={handleSubmit}
  onDemoSelect={handleDemoSelect}
  loading={loading}
/>
```

**Results Display:**
```jsx
<ResultsDisplay
  architecture={architecture}
  scores={scores}
  specification={specification}
  onGenerateCode={handleGenerateCode}
/>
```

**Code Editor:**
```jsx
<MonacoEditor
  files={files}
  selectedFile={selectedFile}
  onFileSelect={handleFileSelect}
  theme={theme}
/>
```

---

## 💻 Code Generation System

### Template Structure

```
backend/code_generation/templates/
├── healthcare_monitoring/
│   └── python/
│       ├── main.py.j2
│       ├── requirements.txt.j2
│       ├── docker-compose.yml.j2
│       ├── Dockerfile.j2
│       ├── README.md.j2
│       └── .env.example.j2
└── ecommerce_recommendation/
    └── python/
        └── ...
```

### Template Variables

```python
{
    "project_name": str,
    "description": str,
    "architecture_type": str,
    "components": List[str],
    "database": str,
    "cache": str,
    "monitoring": bool
}
```

### Code Generation Flow

1. User requests code generation
2. System identifies architecture type
3. Selects appropriate template
4. Renders template with variables
5. Returns generated files
6. User can view/edit in Monaco Editor
7. Download as ZIP file

**Implementation:** [`backend/agents/code_generator_agent.py`](backend/agents/code_generator_agent.py)

---

## 🚀 Deployment Guide

### Local Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python run_backend.py

# Frontend (React)
cd frontend-react
npm install
npm run dev
```

### Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

**Environment Variables:**
```bash
# Backend
GROK_API_KEY=your_api_key
DB_PATH=/data/metamind.db
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com

# Frontend
VITE_API_URL=https://api.yourdomain.com
```

**Docker Compose (Production):**
```yaml
version: '3.8'
services:
  backend:
    image: metamind-backend:latest
    environment:
      - GROK_API_KEY=${GROK_API_KEY}
    volumes:
      - ./data:/data
    restart: always
  
  frontend:
    image: metamind-frontend:latest
    environment:
      - VITE_API_URL=${API_URL}
    ports:
      - "80:80"
    restart: always
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
# Test scoring engine
def test_normalize_cost():
    assert normalize_cost(2500, 5000) == 100.0
    assert normalize_cost(5000, 5000) == 50.0
    assert normalize_cost(7500, 5000) < 50.0

# Test agent output
def test_requirement_agent():
    result = requirement_agent.invoke(input_data)
    assert "parsed_requirements" in result
    assert result["parsed_requirements"]["domain"] in VALID_DOMAINS
```

### Integration Tests

```python
# Test full pipeline
def test_design_pipeline():
    result = graph.invoke(input_state)
    assert result["status"] == "completed"
    assert result["final_architecture"] is not None
    assert 0 <= result["scores"]["final_score"] <= 100
```

### API Tests

```python
# Test endpoints
def test_design_endpoint():
    response = client.post("/api/design", json=payload)
    assert response.status_code == 202
    assert "run_id" in response.json()
```

---

## ⚡ Performance Optimization

### Backend Optimizations

1. **Database Connection Pooling**
```python
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

2. **Async LLM Calls**
```python
async def generate_architectures():
    tasks = [llm.ainvoke(prompt) for prompt in prompts]
    results = await asyncio.gather(*tasks)
    return results
```

3. **Caching**
```python
@lru_cache(maxsize=100)
def get_domain_weights(domain: str):
    return DOMAIN_WEIGHTS.get(domain)
```

### Frontend Optimizations

1. **Code Splitting**
```jsx
const Editor = lazy(() => import('./pages/Editor'));
```

2. **Memoization**
```jsx
const memoizedValue = useMemo(() => 
  computeExpensiveValue(a, b), 
  [a, b]
);
```

3. **Debouncing**
```jsx
const debouncedSearch = useDebouncedCallback(
  (value) => handleSearch(value),
  300
);
```

---

## 📚 Additional Resources

- [API Documentation](http://localhost:8000/docs)
- [Contributing Guide](CONTRIBUTING.md)
- [License](LICENSE)

---

**Last Updated:** 2026-03-05  
**Version:** 1.0.0  
**Maintainer:** MetaMind Team