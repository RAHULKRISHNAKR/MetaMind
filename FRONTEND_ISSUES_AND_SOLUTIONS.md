# MetaMind Frontend Issues & Solutions

## 🐛 Issues Identified

### 1. Score Shows 0.0/100
**Problem**: The final score is not being calculated or returned properly
**Likely Cause**: 
- Scoring engine not being called
- Score not being stored in state
- Frontend not receiving score from API

### 2. Components Show "Unknown"
**Problem**: Architecture modules are not being parsed correctly
**Likely Cause**:
- Architecture generation returning invalid format
- Module structure not matching expected schema
- Frontend parsing logic issue

### 3. Slow Performance (2-5 minutes)
**Problem**: Using local Llama3 model is slow
**Solution**: Switch to Grok API (xAI) for faster responses

---

## ✅ Solution 1: Switch to Grok API

### Step 1: Get Grok API Key
1. Go to https://console.x.ai/
2. Sign up / Log in
3. Create API key
4. Copy the key

### Step 2: Update Environment Variables

Edit `.env` file:
```bash
# Comment out Ollama settings
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3

# Add Grok API settings
XAI_API_KEY=your-api-key-here
XAI_MODEL=grok-beta
LLM_PROVIDER=xai
```

### Step 3: Update LLM Utility

The system needs to be modified to support multiple LLM providers. Here's what needs to change:

**File**: `backend/utils/llm_utils.py`

Add support for:
- OpenAI-compatible API (Grok uses OpenAI format)
- API key authentication
- Provider selection

**File**: `backend/agents/*.py`

Update all agents to use the new provider system.

---

## ✅ Solution 2: Fix Scoring Issue

### Check These Files:

1. **backend/agents/scoring_engine.py**
   - Verify `_calculate_final_score()` is being called
   - Check that score is being stored in state

2. **backend/orchestration/graph.py**
   - Verify scoring engine is in the pipeline
   - Check state flow includes scores

3. **backend/api/main.py**
   - Verify `/api/design/{run_id}/result` returns score
   - Check response format

### Quick Fix:

The score might be stored but not returned. Check the API response structure.

---

## ✅ Solution 3: Fix "Unknown" Components

### Root Cause:

The architecture modules are likely being generated but not properly structured.

### Check These:

1. **backend/agents/architecture_generation_agent.py**
   - Verify module structure matches schema
   - Check JSON parsing

2. **frontend/app.py**
   - Verify component parsing logic
   - Check how modules are displayed

### Expected Module Structure:

```python
{
    "layer": "Data Ingestion",
    "component": "Kafka Streams",
    "config": {
        "throughput": "high",
        "latency": "low"
    }
}
```

---

## 🚀 Quick Workaround: Use API Directly

Instead of using the frontend, test with curl:

```bash
# Start a design
curl -X POST http://localhost:8000/api/design \
  -H "Content-Type: application/json" \
  -d '{
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
    "max_iterations": 1
  }'

# Get the run_id from response, then:
curl http://localhost:8000/api/design/{run_id}/result | jq
```

This will show you the raw JSON response and help identify where the issue is.

---

## 📊 Expected Frontend Output

The frontend should show:

### Design Result Section:
- **Architecture Name**: e.g., "Ecommerce Conversational AI Pipeline"
- **Score**: e.g., "87.5/100"
- **Version**: e.g., "1"

### Performance Metrics (Radar Chart):
- Cost: 85/100
- Latency: 90/100
- Risk: 88/100
- Compliance: 92/100
- Scalability: 85/100
- Complexity: 80/100

### Architecture Details:
- **Template**: e.g., "Fine-Tuned Compact Model Pipeline"
- **Components**: List of modules with:
  - Layer name (e.g., "Data Ingestion")
  - Component name (e.g., "Kafka Streams")
  - Configuration details

### Documentation:
- Executive Summary
- Technical Specification
- Deployment Plan
- Monitoring Strategy

---

## 🔧 Immediate Actions

### 1. Check Backend Logs
```bash
# Look for errors in the terminal running the backend
# Check for:
# - "Scoring complete" messages
# - Architecture generation success
# - Any error messages
```

### 2. Test API Directly
```bash
# Use curl to test the API
# This bypasses frontend issues
curl http://localhost:8000/api/design/{run_id}/result
```

### 3. Check Database
```bash
sqlite3 metamind.db
SELECT * FROM architectures ORDER BY created_at DESC LIMIT 1;
.quit
```

---

## 💡 Performance Comparison

| Provider | Model | Speed | Cost | Quality |
|----------|-------|-------|------|---------|
| **Ollama (Local)** | Llama3 8B | 2-5 min | Free | Good |
| **Ollama (Local)** | Llama3 70B | 10-20 min | Free | Excellent |
| **xAI Grok** | grok-beta | 10-30 sec | $5/1M tokens | Excellent |
| **OpenAI** | GPT-4 | 5-15 sec | $30/1M tokens | Excellent |
| **Anthropic** | Claude 3 | 5-15 sec | $15/1M tokens | Excellent |

**Recommendation**: Switch to Grok API for 10-20x speed improvement.

---

## 🎯 Next Steps

1. **Immediate**: Test API directly with curl to see raw output
2. **Short-term**: Switch to Grok API for speed
3. **Long-term**: Fix frontend parsing and scoring display

---

*This document will be updated as issues are resolved.*