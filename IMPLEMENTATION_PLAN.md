# MetaMind Implementation Plan

## Overview

This document provides a complete implementation roadmap for MetaMind - an autonomous AI pipeline designer that uses recursive multi-agent systems to design, simulate, optimize, and iteratively improve AI architectures.

## Project Structure

```
MetaMind/
├── backend/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── requirement_agent.py
│   │   ├── domain_weight_tuning_agent.py
│   │   ├── architecture_generation_agent.py
│   │   ├── simulation_agent.py
│   │   ├── scoring_engine.py
│   │   ├── optimization_agent.py
│   │   ├── reflection_agent.py
│   │   ├── iteration_agent.py
│   │   ├── versioning_agent.py
│   │   ├── comparison_agent.py
│   │   └── spec_generator_agent.py
│   ├── orchestration/
│   │   ├── __init__.py
│   │   ├── state.py ✅ COMPLETED
│   │   └── graph.py ✅ COMPLETED
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── templates.py
│   │   ├── cost_estimator.py
│   │   └── helpers.py
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   ├── pages/
│   │   ├── 1_design.py
│   │   ├── 2_results.py
│   │   ├── 3_history.py
│   │   └── 4_comparison.py
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example
├── METAMIND_ARCHITECTURE.md ✅ COMPLETED
├── IMPLEMENTATION_PLAN.md ✅ CURRENT
└── README.md
```

## Phase 1: Core Agent Implementation

### 1.1 RequirementAgent (LLM-based)
**File**: `backend/agents/requirement_agent.py`

**Purpose**: Parse natural language requirements into structured JSON

**Key Features**:
- LLM prompt engineering for requirement extraction
- Validation of extracted constraints
- Default value assignment for missing fields
- Error handling for ambiguous inputs

**Implementation Steps**:
1. Create LangChain LLM wrapper for Ollama
2. Design prompt template with examples
3. Implement JSON parsing and validation
4. Add error handling and fallbacks

### 1.2 DomainWeightTuningAgent (Rule-based)
**File**: `backend/agents/domain_weight_tuning_agent.py`

**Purpose**: Map domain to optimization weights

**Key Features**:
- Predefined weight mappings for each domain
- Weight validation (must sum to 1.0)
- Custom weight override support

**Implementation Steps**:
1. Define DOMAIN_WEIGHTS dictionary
2. Implement weight lookup logic
3. Add weight validation
4. Support custom weight overrides

### 1.3 ArchitectureGenerationAgent (LLM-based)
**File**: `backend/agents/architecture_generation_agent.py`

**Purpose**: Generate 3-5 candidate architectures using templates

**Key Features**:
- Template-based generation
- Module selection from predefined components
- Topology specification (sequential, parallel, hierarchical)
- Configuration parameter assignment

**Implementation Steps**:
1. Load architecture templates
2. Create LLM prompt with constraints
3. Parse LLM output into Architecture objects
4. Validate generated architectures
5. Ensure diversity in candidates

### 1.4 SimulationAgent (Hybrid)
**File**: `backend/agents/simulation_agent.py`

**Purpose**: Estimate metrics for each architecture

**Key Features**:
- Cost estimation (model + infrastructure)
- Latency estimation (based on topology)
- Risk assessment (LLM-based)
- Compliance checking (rule-based + LLM)
- Scalability analysis
- Complexity calculation

**Implementation Steps**:
1. Implement cost estimation rules
2. Create latency estimation model
3. Build risk assessment LLM prompt
4. Implement compliance checker
5. Add scalability analyzer
6. Create complexity calculator

### 1.5 DeterministicScoringEngine (Rule-based)
**File**: `backend/agents/scoring_engine.py`

**Purpose**: Normalize metrics and compute weighted scores

**Key Features**:
- Metric normalization (0-100 scale)
- Weighted score calculation
- Deterministic and reproducible
- Configurable normalization curves

**Implementation Steps**:
1. Implement normalization functions for each metric
2. Create weighted scoring formula
3. Add score validation
4. Implement score explanation generation

### 1.6 OptimizationAgent (Rule-based)
**File**: `backend/agents/optimization_agent.py`

**Purpose**: Select highest scoring architecture

**Key Features**:
- Simple sorting by final score
- Tie-breaking logic
- Selection justification

**Implementation Steps**:
1. Sort candidates by score
2. Implement tie-breaking rules
3. Generate selection justification

### 1.7 ReflectionAgent (LLM-based)
**File**: `backend/agents/reflection_agent.py`

**Purpose**: Critique selected architecture and suggest improvements

**Key Features**:
- Strength/weakness analysis
- Confidence scoring (0.0-1.0)
- Specific improvement suggestions
- Iteration decision logic

**Implementation Steps**:
1. Create reflection prompt template
2. Implement LLM-based critique
3. Parse reflection output
4. Calculate confidence score
5. Generate improvement suggestions

### 1.8 IterationAgent (Hybrid)
**File**: `backend/agents/iteration_agent.py`

**Purpose**: Apply improvements to architecture

**Key Features**:
- Rule-based improvement application
- Module addition/replacement
- Configuration tuning
- Change tracking

**Implementation Steps**:
1. Parse improvement suggestions
2. Implement improvement rules
3. Apply changes to architecture
4. Track changes made
5. Validate improved architecture

### 1.9 VersioningAgent (Rule-based)
**File**: `backend/agents/versioning_agent.py`

**Purpose**: Store architecture versions in database

**Key Features**:
- Version record creation
- Database persistence
- Parent-child version linking
- Metadata storage

**Implementation Steps**:
1. Create database schema
2. Implement version record creation
3. Add database storage logic
4. Implement version retrieval

### 1.10 ComparisonAgent (Rule-based)
**File**: `backend/agents/comparison_agent.py`

**Purpose**: Compare two architecture versions

**Key Features**:
- Metric delta calculation
- Score improvement analysis
- Change summary
- Recommendation generation

**Implementation Steps**:
1. Implement delta calculation
2. Create comparison summary
3. Generate recommendations
4. Format comparison output

### 1.11 SpecGeneratorAgent (LLM-based)
**File**: `backend/agents/spec_generator_agent.py`

**Purpose**: Generate comprehensive documentation

**Key Features**:
- Executive summary
- Technical specification
- Deployment plan
- Monitoring strategy

**Implementation Steps**:
1. Create documentation prompt templates
2. Implement LLM-based generation
3. Format output as markdown
4. Add PDF export capability

## Phase 2: Supporting Infrastructure

### 2.1 Database Layer
**File**: `backend/database/db.py`

**Schema**:
```sql
-- Runs table
CREATE TABLE runs (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    business_goal TEXT NOT NULL,
    domain VARCHAR(50) NOT NULL,
    constraints_json JSONB NOT NULL,
    weights_json JSONB NOT NULL,
    final_architecture_id UUID,
    status VARCHAR(20) NOT NULL,
    INDEX idx_timestamp (timestamp)
);

-- Architectures table
CREATE TABLE architectures (
    id UUID PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES runs(id),
    version INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    architecture_json JSONB NOT NULL,
    metrics_json JSONB NOT NULL,
    score FLOAT NOT NULL,
    changes_made TEXT[],
    parent_version INTEGER,
    INDEX idx_run_id (run_id),
    INDEX idx_version (run_id, version)
);
```

### 2.2 Utility Modules

#### templates.py
- Architecture template definitions
- Module component catalog
- Configuration schemas

#### cost_estimator.py
- Model pricing tables
- Infrastructure cost calculations
- Monthly projection logic

#### helpers.py
- JSON validation
- UUID generation
- Timestamp formatting
- Error handling utilities

## Phase 3: FastAPI Backend

### 3.1 API Endpoints
**File**: `backend/api/main.py`

```python
# Core endpoints
POST   /api/design              # Start new design session
GET    /api/design/{run_id}/status
GET    /api/design/{run_id}/candidates
GET    /api/design/{run_id}/result
GET    /api/design/{run_id}/versions
GET    /api/design/{run_id}/compare/{v1}/{v2}
GET    /api/design/{run_id}/specification
GET    /api/history
GET    /api/health
```

### 3.2 Request/Response Models

```python
class DesignRequest(BaseModel):
    business_goal: str
    domain: str
    modalities: List[str]
    constraints: Dict[str, Any]
    max_iterations: int = 5

class DesignResponse(BaseModel):
    run_id: str
    status: str
    message: str

class ResultResponse(BaseModel):
    run_id: str
    version: int
    selected_architecture: Dict
    metrics: Dict
    score: float
    reflection: Dict
    specification: str
```

## Phase 4: Streamlit Frontend

### 4.1 Main App
**File**: `frontend/app.py`

**Features**:
- Navigation sidebar
- Session state management
- API client wrapper
- Error handling

### 4.2 Design Page
**File**: `frontend/pages/1_design.py`

**Components**:
- Business goal text input
- Domain dropdown
- Modality checkboxes
- Constraint sliders
- Submit button
- Progress indicator

### 4.3 Results Page
**File**: `frontend/pages/2_results.py`

**Components**:
- Selected architecture card
- Metrics radar chart
- Score breakdown
- Reflection analysis
- Download specification button

### 4.4 History Page
**File**: `frontend/pages/3_history.py`

**Components**:
- Run history table
- Filter controls
- Run detail view
- Delete run button

### 4.5 Comparison Page
**File**: `frontend/pages/4_comparison.py`

**Components**:
- Version selector
- Side-by-side architecture view
- Metric delta table
- Score improvement chart
- Change summary

## Phase 5: Deployment

### 5.1 Docker Configuration

**Dockerfile.backend**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Dockerfile.frontend**:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY frontend/ .
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_BASE_URL=http://host.docker.internal:11434
      - DATABASE_URL=postgresql://user:pass@db:5432/metamind
    depends_on:
      - db
  
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "8501:8501"
    environment:
      - BACKEND_URL=http://backend:8000
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=metamind
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 5.2 Environment Configuration

**.env.example**:
```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Database Configuration
DATABASE_URL=postgresql://user:pass@localhost:5432/metamind

# API Configuration
BACKEND_PORT=8000
FRONTEND_PORT=8501

# Application Settings
MAX_ITERATIONS=5
CONFIDENCE_THRESHOLD=0.85
```

## Phase 6: Testing & Documentation

### 6.1 Unit Tests
- Test each agent independently
- Mock LLM responses
- Validate state transformations
- Test scoring logic

### 6.2 Integration Tests
- Test complete pipeline
- Verify database operations
- Test API endpoints
- Validate frontend integration

### 6.3 Documentation
- API documentation (OpenAPI/Swagger)
- User guide
- Developer guide
- Architecture diagrams

## Implementation Timeline

### Week 1: Core Agents (Phase 1)
- Day 1-2: RequirementAgent, DomainWeightTuningAgent
- Day 3-4: ArchitectureGenerationAgent, SimulationAgent
- Day 5-7: ScoringEngine, OptimizationAgent, ReflectionAgent

### Week 2: Iteration & Versioning
- Day 1-2: IterationAgent
- Day 3-4: VersioningAgent, ComparisonAgent
- Day 5-7: SpecGeneratorAgent, Database layer

### Week 3: Backend API (Phase 3)
- Day 1-3: FastAPI endpoints
- Day 4-5: Request/response models
- Day 6-7: Error handling, validation

### Week 4: Frontend (Phase 4)
- Day 1-2: Main app, Design page
- Day 3-4: Results page, History page
- Day 5-7: Comparison page, UI polish

### Week 5: Deployment & Testing (Phases 5-6)
- Day 1-2: Docker configuration
- Day 3-4: Integration testing
- Day 5-7: Documentation, final polish

## Success Criteria

✅ **Functional Requirements**:
1. System generates 3-5 distinct architectures per request
2. Scoring is deterministic and reproducible
3. Reflection confidence threshold triggers iteration
4. Version history tracks all improvements
5. Comparison shows measurable metric deltas
6. Final specification is production-ready

✅ **Non-Functional Requirements**:
1. End-to-end design completes in < 5 minutes
2. API response time < 2 seconds (excluding LLM calls)
3. Frontend is responsive and intuitive
4. System handles errors gracefully
5. All data is persisted in database
6. Docker deployment works out-of-box

## Next Steps

1. ✅ Architecture design completed
2. ✅ State schema implemented
3. ✅ Orchestration graph created
4. 🔄 Implement core agents (in progress)
5. ⏳ Build deterministic scoring engine
6. ⏳ Implement reflection and iteration loop
7. ⏳ Create versioning and comparison system
8. ⏳ Design and implement FastAPI backend
9. ⏳ Build Streamlit frontend with visualization
10. ⏳ Create comprehensive documentation
11. ⏳ Set up Docker deployment configuration

---

**MetaMind** - Building the Future of AI Architecture Design