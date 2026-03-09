# 🚀 Getting Started with MetaMind

This guide will help you set up and run MetaMind on your local machine or deploy it to production.

---

## 📋 Prerequisites

### Required
- **Docker** and **Docker Compose** (recommended)
- **Groq API Key** - Free at [console.groq.com](https://console.groq.com/)

### For Local Development (Optional)
- **Python 3.11+**
- **Node.js 18+**
- **Git**

---

## ⚡ Quick Start (Docker - Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/metamind.git
cd metamind
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key
nano .env
```

Add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Start All Services

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Access the Application

- **React Frontend**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🎯 Try Demo Mode

The fastest way to see MetaMind in action:

1. Open http://localhost:5173
2. Click the **"Try Demo"** button
3. Select a pre-configured scenario:
   - 🏥 **Healthcare Patient Monitoring**
   - 🛒 **E-commerce Recommendation Engine**
4. Get instant results with production-ready code!

---

## 💻 Local Development Setup

For development without Docker:

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python run_backend.py
```

Backend will be available at: http://localhost:8000

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend-react

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: http://localhost:5173

---

## 🎨 Using the Application

### 1. Design Custom Architecture

1. Fill in the design form:
   - **Business Goal**: "Build a customer support chatbot"
   - **Domain**: E-commerce
   - **Modalities**: Text
   - **Constraints**: Budget, latency, users, risk, compliance

2. Click **"🚀 Design Architecture"**

3. Watch real-time progress through 11 agent steps

4. View results with interactive visualizations

5. Generate production-ready code

6. Download complete project as ZIP

### 2. Use the API Directly

```bash
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
    "max_iterations": 3
  }'
```

### 3. View API Documentation

Visit http://localhost:8000/docs for interactive API documentation with:
- All available endpoints
- Request/response schemas
- Try-it-out functionality
- Example requests

---

## 📊 Understanding the Output

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

## 🔧 Configuration

### Environment Variables

Edit `.env` file:

```env
# LLM Provider
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# Alternative providers (optional)
# XAI_API_KEY=your_xai_key
# OPENAI_API_KEY=your_openai_key
# ANTHROPIC_API_KEY=your_anthropic_key

# Database
DB_PATH=./metamind.db

# Server
PORT=8000
LOG_LEVEL=INFO

# CORS (for production)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Domain Weights Customization

Edit `backend/agents/domain_weight_tuning_agent.py`:

```python
DOMAIN_WEIGHTS = {
    "your_domain": {
        "cost": 0.15,
        "latency": 0.20,
        "risk": 0.25,
        "compliance": 0.20,
        "scalability": 0.15,
        "complexity": 0.05
    }
}
```

---

## 🧪 Testing

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Test design endpoint
curl -X POST http://localhost:8000/api/design \
  -H "Content-Type: application/json" \
  -d @test_request.json
```

### Test Frontend

```bash
cd frontend-react
npm run test
```

---

## 🐛 Troubleshooting

### Issue: "Connection refused" to backend

**Solution**:
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not, start it
docker-compose up -d backend
# Or for local development:
cd backend && python run_backend.py
```

### Issue: "Invalid API key"

**Solution**:
1. Verify your API key in `.env` file
2. Get a new key from [console.groq.com](https://console.groq.com/)
3. Restart the backend: `docker-compose restart backend`

### Issue: Frontend not loading

**Solution**:
```bash
# Check if frontend is running
curl http://localhost:5173

# Restart frontend
docker-compose restart frontend-react
# Or for local development:
cd frontend-react && npm run dev
```

### Issue: Slow performance

**Causes**:
- Large model (70B instead of 8B)
- Network latency to Groq API
- Low system resources

**Solutions**:
```bash
# Use smaller model in .env
GROQ_MODEL=llama-3.1-8b-instant

# Reduce max iterations in request
"max_iterations": 2

# Close other applications to free up resources
```

---

## 📁 Project Structure

```
MetaMind/
├── backend/
│   ├── agents/          # 11 specialized agents
│   ├── orchestration/   # LangGraph pipeline
│   ├── api/            # FastAPI endpoints
│   ├── utils/          # Utilities
│   └── requirements.txt
├── frontend-react/
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API client
│   │   └── types/      # TypeScript types
│   └── package.json
├── k8s/                # Kubernetes manifests
├── docs/               # Documentation
├── docker-compose.yml  # Docker Compose config
├── .env.example        # Environment template
└── README.md          # Project overview
```

---

## 🚀 Next Steps

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
   - Modify domain weights
   - Add new architecture templates
   - Adjust scoring curves

4. **Deploy to Production**
   - See [Deployment Guide](DEPLOYMENT.md)
   - Configure Kubernetes
   - Set up monitoring

---

## 📚 Additional Resources

- [Architecture Documentation](ARCHITECTURE.md)
- [API Reference](API_REFERENCE.md)
- [Development Guide](DEVELOPMENT.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

---

## 🆘 Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. View logs: `docker-compose logs -f`
3. Check API health: `curl http://localhost:8000/health`
4. Open an issue on [GitHub](https://github.com/yourusername/metamind/issues)

---

**Ready to design AI architectures!** 🎉