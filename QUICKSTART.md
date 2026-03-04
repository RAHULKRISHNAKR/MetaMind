# MetaMind - Local Setup Guide

This guide will help you run MetaMind locally on your machine.

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.11+**
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **Ollama** (for running Llama 3 locally)
   - Download from: https://ollama.ai/
   - Or install via:
     ```bash
     # macOS
     brew install ollama
     
     # Linux
     curl -fsSL https://ollama.com/install.sh | sh
     ```

3. **Git** (to clone the repository)

---

## Step-by-Step Setup

### 1. Install and Start Ollama

```bash
# Start Ollama service
ollama serve

# In a new terminal, pull the Llama 3 model
ollama pull llama3

# Verify it's working
ollama list
```

**Note**: Keep the `ollama serve` terminal running throughout.

### 2. Clone the Repository

```bash
cd ~/Documents/github/Personal_Project
# The MetaMind folder should already be there
cd MetaMind
```

### 3. Set Up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Verify activation (you should see (venv) in your prompt)
```

### 4. Install Dependencies

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
pip list | grep langchain
```

### 5. Configure Environment

```bash
# Go back to project root
cd ..

# Copy environment template
cp .env.example .env

# The default values should work for local development:
# OLLAMA_BASE_URL=http://localhost:11434
# OLLAMA_MODEL=llama3
# DB_PATH=./metamind.db
# PORT=8000
```

### 6. Create Required Directories

```bash
# Create __init__.py files if missing
touch backend/__init__.py
touch backend/orchestration/__init__.py
touch backend/api/__init__.py
```

### 7. Start the Backend Server

```bash
# From the MetaMind root directory
cd backend
python -m api.main

# You should see:
# INFO:     Started server process
# INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal running!**

### 8. Test the API

Open a new terminal and test:

```bash
# Test health endpoint
curl http://localhost:8000/health

# You should see:
# {"status":"healthy","ollama_url":"http://localhost:11434","model":"llama3","database":"./metamind.db"}

# View API documentation
open http://localhost:8000/docs
# Or visit in browser: http://localhost:8000/docs
```

---

## Running Your First Design

### Option 1: Using curl

```bash
curl -X POST http://localhost:8000/api/design \
  -H "Content-Type: application/json" \
  -d '{
    "business_goal": "Build a customer support chatbot for e-commerce",
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
  }'
```

This will take 2-5 minutes to complete. You'll get a response with a `run_id`.

### Option 2: Using the API Docs

1. Go to http://localhost:8000/docs
2. Click on `POST /api/design`
3. Click "Try it out"
4. Use this example request:

```json
{
  "business_goal": "Build a customer support chatbot for e-commerce",
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
```

5. Click "Execute"
6. Copy the `run_id` from the response

### Option 3: Using Python

Create a file `test_metamind.py`:

```python
import requests
import json

# Design request
response = requests.post(
    "http://localhost:8000/api/design",
    json={
        "business_goal": "Build a customer support chatbot for e-commerce",
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
)

result = response.json()
print(f"Design started! Run ID: {result['run_id']}")
print(f"Status: {result['status']}")

# Get the result
run_id = result['run_id']
result_response = requests.get(f"http://localhost:8000/api/design/{run_id}/result")
design_result = result_response.json()

print(f"\nSelected Architecture: {design_result['selected_architecture']['name']}")
print(f"Final Score: {design_result['score']:.1f}/100")
print(f"\nMetrics:")
for metric, value in design_result['metrics'].items():
    print(f"  {metric}: {value:.1f}")
```

Run it:
```bash
python test_metamind.py
```

---

## Viewing Results

### Get Design Result

```bash
# Replace {run_id} with your actual run_id
curl http://localhost:8000/api/design/{run_id}/result | jq
```

### Get All Versions

```bash
curl http://localhost:8000/api/design/{run_id}/versions | jq
```

### Compare Versions

```bash
# Compare version 1 and version 2
curl http://localhost:8000/api/design/{run_id}/compare/1/2 | jq
```

### Get Complete Specification

```bash
curl http://localhost:8000/api/design/{run_id}/specification | jq
```

### View History

```bash
curl http://localhost:8000/api/history | jq
```

---

## Understanding the Output

When you run a design, MetaMind will:

1. **Parse Requirements** (2-3 seconds)
   - Converts your natural language to structured constraints

2. **Tune Weights** (<1 second)
   - Sets optimization priorities based on domain

3. **Generate Architectures** (30-60 seconds)
   - Creates 3-5 distinct candidate architectures

4. **Simulate Metrics** (20-40 seconds per candidate)
   - Estimates cost, latency, risk, compliance, scalability, complexity

5. **Score & Select** (<1 second)
   - Normalizes metrics and selects optimal architecture

6. **Reflect** (10-20 seconds)
   - Critiques the selection and assesses confidence

7. **Iterate** (if confidence < 0.85)
   - Improves architecture and repeats simulation
   - Can iterate up to `max_iterations` times

8. **Generate Documentation** (30-60 seconds)
   - Creates executive summary, technical spec, deployment plan, monitoring strategy

**Total Time**: 2-5 minutes depending on iterations

---

## Troubleshooting

### Issue: "Connection refused" to Ollama

**Solution**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### Issue: "Model not found"

**Solution**:
```bash
# Pull the Llama 3 model
ollama pull llama3

# Verify
ollama list
```

### Issue: "Module not found" errors

**Solution**:
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
cd backend
pip install -r requirements.txt
```

### Issue: "Database locked" error

**Solution**:
```bash
# Stop the backend server (Ctrl+C)
# Delete the database file
rm metamind.db
# Restart the server
python -m api.main
```

### Issue: Slow performance

**Causes**:
- Ollama using CPU instead of GPU
- Large model (70B instead of 8B)
- Low system resources

**Solutions**:
```bash
# Use smaller model
export OLLAMA_MODEL=llama3:8b

# Reduce max iterations
# In your request, set "max_iterations": 2

# Close other applications to free up RAM
```

---

## Project Structure

```
MetaMind/
├── backend/
│   ├── agents/          # 11 specialized agents
│   ├── orchestration/   # LangGraph pipeline
│   ├── api/            # FastAPI endpoints
│   └── requirements.txt
├── .env.example        # Environment template
├── QUICKSTART.md       # This file
└── README.md          # Project overview
```

---

## Next Steps

1. **Explore the API**
   - Visit http://localhost:8000/docs
   - Try different domains (healthcare, finance, education)
   - Experiment with different constraints

2. **View the Database**
   ```bash
   sqlite3 metamind.db
   .tables
   SELECT * FROM runs;
   .quit
   ```

3. **Customize**
   - Modify domain weights in `backend/agents/domain_weight_tuning_agent.py`
   - Add new architecture templates in `backend/agents/architecture_generation_agent.py`
   - Adjust scoring curves in `backend/agents/scoring_engine.py`

---

## Stopping the Server

```bash
# In the terminal running the backend:
Ctrl+C

# Deactivate virtual environment:
deactivate

# Stop Ollama (if desired):
# Find the process and kill it, or just close the terminal
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `ollama serve` | Start Ollama service |
| `source venv/bin/activate` | Activate Python environment |
| `python run_backend.py` | Start MetaMind backend |
| `curl http://localhost:8000/health` | Check if API is running |
| `open http://localhost:8000/docs` | View API documentation |

---

## Support

If you encounter issues:

1. Check the terminal output for error messages
2. Verify Ollama is running: `curl http://localhost:11434/api/tags`
3. Verify Python environment: `which python` (should show venv path)
4. Check the logs in the backend terminal

---

**MetaMind** - Autonomous AI Pipeline Designer

*Ready to design AI architectures!*