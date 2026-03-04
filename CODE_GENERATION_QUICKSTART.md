# 🚀 Code Generation Quick Start Guide

**MetaMind Phase 1: Interactive Builder**

This guide will help you test the new code generation feature that transforms MetaMind architecture designs into production-ready code.

---

## 📋 Prerequisites

1. **Backend running** on `http://localhost:8000`
2. **Frontend running** on `http://localhost:8501`
3. **Jinja2 installed**: `pip install jinja2==3.1.4`

---

## 🎯 Quick Test (5 Minutes)

### Step 1: Start the System

```bash
# Terminal 1 - Backend
cd /Users/rahukkrishnakr/Documents/github/MetaMind
python run_backend.py

# Terminal 2 - Frontend
python run_frontend.py
```

### Step 2: Create a Design

1. Open browser: `http://localhost:8501`
2. Fill in the design form:
   - **Business Goal:** "Build a customer support chatbot with document search"
   - **Domain:** Healthcare
   - **Modalities:** Text
   - **Constraints:**
     - Budget: Medium
     - Latency: Low
     - Compliance: High
3. Click **"🚀 Start Design"**
4. Wait for design to complete (~30-60 seconds)

### Step 3: Generate Code

1. Scroll down to **"🚀 Generate Production Code"** section
2. Enter project name: `customer_support_bot`
3. Click **"🚀 Generate Code"** button
4. Wait for generation (~2 seconds)
5. See success message with file list
6. Click **"📥 Download ZIP Archive"**

### Step 4: Test Generated Code

```bash
# Extract the ZIP
cd ~/Downloads
unzip customer_support_bot.zip
cd customer_support_bot

# Review the files
ls -la
# You should see:
# - main.py
# - requirements.txt
# - Dockerfile
# - docker-compose.yml
# - .env
# - README.md

# Install dependencies
pip install -r requirements.txt

# Configure environment (if using OpenAI)
nano .env
# Add your OPENAI_API_KEY

# Run the application
python main.py

# Test the API (in another terminal)
curl http://localhost:8000/health
```

---

## 🧪 What to Test

### ✅ Frontend UI
- [ ] "Generate Code" button appears after design completes
- [ ] Project name input field works
- [ ] Generation shows progress spinner
- [ ] Success message displays
- [ ] File list expands and shows all files
- [ ] Download button appears with gradient styling
- [ ] Next steps guide is visible

### ✅ Generated Files
- [ ] `main.py` - Complete FastAPI application
- [ ] `requirements.txt` - All dependencies listed
- [ ] `Dockerfile` - Valid Docker configuration
- [ ] `docker-compose.yml` - Multi-container setup
- [ ] `.env` - Environment variables template
- [ ] `README.md` - Comprehensive documentation

### ✅ Generated Code Quality
- [ ] Code runs without errors
- [ ] Health endpoint responds: `GET /health`
- [ ] API documentation available: `http://localhost:8000/docs`
- [ ] Can add documents: `POST /documents`
- [ ] Can query: `POST /query`
- [ ] Docker build succeeds: `docker build -t test .`
- [ ] Docker compose works: `docker-compose up`

### ✅ API Endpoints
- [ ] `POST /api/design/{run_id}/generate-code` - Returns 200
- [ ] Response includes `download_url`
- [ ] Response includes `files_generated` list
- [ ] `GET /api/design/{run_id}/download/{project_id}` - Downloads ZIP
- [ ] ZIP file is valid and extractable

---

## 🐛 Common Issues & Solutions

### Issue 1: "Templates directory not found"
**Solution:** Ensure templates exist:
```bash
ls -la backend/code_generation/templates/rag_pipeline/python/
```

### Issue 2: "Jinja2 not installed"
**Solution:** Install Jinja2:
```bash
pip install jinja2==3.1.4
```

### Issue 3: "Cannot connect to backend"
**Solution:** Check backend is running:
```bash
curl http://localhost:8000/health
```

### Issue 4: Generated code fails to run
**Solution:** Check Python version and dependencies:
```bash
python --version  # Should be 3.11+
pip install -r requirements.txt
```

### Issue 5: Docker build fails
**Solution:** Check Docker is installed and running:
```bash
docker --version
docker ps
```

---

## 📊 Expected Results

### Generation Performance
- **Template Rendering:** < 100ms
- **File Writing:** < 200ms
- **ZIP Creation:** < 300ms
- **Total Time:** < 2 seconds

### Generated Project
- **Files:** 6 files
- **Total Size:** 10-50 KB (uncompressed)
- **ZIP Size:** 5-15 KB (compressed)
- **Lines of Code:** ~800 lines

### Generated Code Features
- ✅ FastAPI REST API
- ✅ LangChain RAG pipeline
- ✅ ChromaDB vector store
- ✅ Health check endpoint
- ✅ Document ingestion
- ✅ Query endpoint
- ✅ Docker support
- ✅ Environment configuration
- ✅ Comprehensive README

---

## 🎨 UI Screenshots (Expected)

### Before Generation
```
┌─────────────────────────────────────────┐
│  🚀 Generate Production Code            │
│                                         │
│  Transform your architecture design     │
│  into production-ready code!            │
│                                         │
│  Project Name: [my_ai_pipeline____]    │
│                                         │
│  [🚀 Generate Code]                     │
└─────────────────────────────────────────┘
```

### After Generation
```
┌─────────────────────────────────────────┐
│  ✅ Successfully generated 6 files      │
│                                         │
│  Architecture Type: rag_pipeline        │
│  Files Generated: 6                     │
│                                         │
│  📁 Generated Files                     │
│    ✓ main.py                           │
│    ✓ requirements.txt                  │
│    ✓ Dockerfile                        │
│    ✓ docker-compose.yml                │
│    ✓ .env                              │
│    ✓ README.md                         │
│                                         │
│  [📥 Download ZIP Archive]             │
│                                         │
│  🎯 Next Steps                          │
│  1. Extract the ZIP file               │
│  2. Configure .env                     │
│  3. Install dependencies               │
│  4. Run: python main.py                │
│  5. Deploy: docker-compose up          │
└─────────────────────────────────────────┘
```

---

## 📝 Test Checklist

### Pre-Test Setup
- [ ] Backend running on port 8000
- [ ] Frontend running on port 8501
- [ ] Jinja2 installed
- [ ] Templates directory exists
- [ ] API endpoints accessible

### Functional Tests
- [ ] Can create a design
- [ ] Design completes successfully
- [ ] Generate button appears
- [ ] Can enter project name
- [ ] Generation succeeds
- [ ] File list displays
- [ ] Can download ZIP
- [ ] ZIP extracts correctly
- [ ] Generated code runs
- [ ] API endpoints work

### Edge Cases
- [ ] Empty project name (should show error)
- [ ] Special characters in project name
- [ ] Generate before design completes (should show error)
- [ ] Generate for non-existent run_id (should 404)
- [ ] Multiple generations for same design
- [ ] Large project names (>100 chars)

### Performance Tests
- [ ] Generation completes in < 5 seconds
- [ ] ZIP download is fast
- [ ] No memory leaks
- [ ] Can generate multiple projects concurrently

---

## 🎓 What You Should See

### 1. Successful Generation Log (Backend)
```
🚀 Starting code generation for: customer_support_bot
📋 Detected architecture type: rag_pipeline
✅ Generated: main.py
✅ Generated: requirements.txt
✅ Generated: Dockerfile
✅ Generated: docker-compose.yml
✅ Generated: .env
✅ Generated: README.md
✅ Generated 6 files
✅ Created ZIP archive: ./generated_projects/customer_support_bot.zip
```

### 2. API Response
```json
{
  "status": "success",
  "project_path": "./generated_projects/customer_support_bot",
  "files_generated": [
    "main.py",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    ".env",
    "README.md"
  ],
  "architecture_type": "rag_pipeline",
  "message": "Successfully generated 6 files for customer_support_bot",
  "download_url": "/api/design/abc123/download/abc123_customer_support_bot"
}
```

### 3. Generated main.py (Sample)
```python
"""
customer_support_bot
Generated by MetaMind - AI Pipeline Designer

A production-ready RAG (Retrieval-Augmented Generation) pipeline
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# ... (complete working code)
```

---

## 🚀 Next Steps After Testing

### If Everything Works ✅
1. Mark Phase 1 as complete
2. Gather user feedback
3. Consider Phase 2 implementation
4. Add more architecture templates

### If Issues Found ❌
1. Document the issue
2. Check logs for errors
3. Verify template syntax
4. Test with different architectures
5. Fix and re-test

---

## 📞 Support

### Logs to Check
- **Backend:** Terminal running `run_backend.py`
- **Frontend:** Terminal running `run_frontend.py`
- **Generated Code:** `./generated_projects/{project_name}/`

### Debug Commands
```bash
# Check backend health
curl http://localhost:8000/health

# List generated projects
ls -la ./generated_projects/

# View backend logs
# (Check terminal running run_backend.py)

# Test template rendering manually
cd backend/agents
python code_generator_agent.py
```

---

## ✅ Success Criteria

Phase 1 is successful if:
- ✅ User can generate code with one click
- ✅ Generated code is complete and runnable
- ✅ ZIP download works
- ✅ Documentation is comprehensive
- ✅ Generation takes < 5 seconds
- ✅ No errors in logs
- ✅ Docker deployment works

---

**Ready to test? Let's go! 🚀**

*For detailed implementation details, see `PHASE_1_COMPLETION_REPORT.md`*