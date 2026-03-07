# 🧠 MetaMind

**Autonomous AI Pipeline Designer & Self-Optimizing Architecture Engine**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3.1-61DAFB.svg)](https://reactjs.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5.svg)](https://kubernetes.io/)

MetaMind is a cutting-edge **multi-agent AI system** that autonomously designs, simulates, optimizes, and iteratively improves AI pipelines under real-world constraints. It combines LLM reasoning with deterministic scoring to create production-ready AI architectures.

---

## ✨ Key Features

🤖 **11 Specialized AI Agents** - Orchestrated via LangGraph for intelligent pipeline design  
🎯 **Domain-Adaptive Optimization** - Healthcare, Finance, E-commerce, and more  
📊 **Deterministic Scoring** - 6 metrics (Cost, Latency, Risk, Compliance, Scalability, Complexity)  
🔄 **Self-Improvement Loop** - Automatic reflection and iterative refinement  
💻 **Production-Ready Code** - Generate complete applications with Docker, monitoring, and docs  
🎨 **Modern React UI** - Beautiful interface with Monaco Editor integration
🚀 **Demo Mode** - Instant results for presentations and testing
☸️ **Kubernetes Ready** - Production-grade K8s manifests with automated deployment

---

## 🚀 Quick Start

### Option 1: Kubernetes (Production-Ready)

```bash
# Prerequisites: Docker, Minikube/K8s cluster, kubectl
# Get your free API key from https://console.groq.com/

# Clone repository
git clone https://github.com/yourusername/metamind.git
cd metamind

# Configure API key
nano k8s/secret.yaml
# Replace 'your-groq-api-key-here' with your actual key

# Deploy to Kubernetes
cd k8s
./deploy.sh

# Access the application
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
# Visit: http://localhost:8080
```

**📚 Complete Kubernetes Guide**: See [`k8s/QUICKSTART.md`](k8s/QUICKSTART.md) for detailed instructions

### Option 2: Docker Compose (Quick Testing)

```bash
# Clone repository
git clone https://github.com/yourusername/metamind.git
cd metamind

# Set up environment
cp .env.example .env
# Edit .env and add your GROK_API_KEY

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- Grok API key (or Ollama with Llama 3)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python run_backend.py
```

**Frontend:**
```bash
cd frontend-react
npm install
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

---

## 🎯 Usage

### 1. Try Demo Mode (Fastest)

1. Open http://localhost:5173
2. Click **"Try Demo"** button
3. Select a pre-configured scenario:
   - 🏥 Healthcare Patient Monitoring
   - 🛒 E-commerce Recommendation Engine
4. Get instant results with production-ready code

### 2. Design Custom Architecture

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

### 3. Use API Directly

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

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER BROWSER                          │
│              http://localhost:5173                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              REACT FRONTEND (Vite)                       │
│  • Interactive Forms    • Monaco Editor                  │
│  • Real-time Progress   • Code Generation                │
└────────────────────┬────────────────────────────────────┘
                     │ REST API
                     ▼
┌─────────────────────────────────────────────────────────┐
│               FASTAPI BACKEND                            │
│              http://localhost:8000                       │
│  • 10 REST Endpoints  • Request Validation               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│            LANGGRAPH ORCHESTRATOR                        │
│  • 11 Specialized Agents  • State Management             │
│  • Conditional Routing    • Iteration Control            │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────┐         ┌──────────────┐
│  Grok API    │         │   SQLITE DB  │
│  (or Ollama) │         │  (Versions)  │
└──────────────┘         └──────────────┘
```

---

## 🧩 11 Specialized Agents

1. **RequirementAgent** - Parse natural language to structured JSON
2. **DomainWeightTuningAgent** - Map domain to optimization weights
3. **ArchitectureGenerationAgent** - Generate 3-5 candidates from templates
4. **SimulationAgent** - Estimate 6 metrics per candidate
5. **DeterministicScoringEngine** - Normalize metrics to 0-100 scale
6. **OptimizationAgent** - Select highest scoring architecture
7. **ReflectionAgent** - Critique with confidence scoring (0.0-1.0)
8. **IterationAgent** - Apply improvements based on reflection
9. **VersioningAgent** - Store versions in database
10. **ComparisonAgent** - Calculate version deltas
11. **SpecGeneratorAgent** - Generate comprehensive documentation

---

## 📊 Evaluation Metrics

| Metric | Description | Optimization |
|--------|-------------|--------------|
| **Cost** | Infrastructure + operational costs | Lower is better |
| **Latency** | Response time performance | Lower is better |
| **Risk** | Security and reliability risks | Lower is better |
| **Compliance** | Regulatory adherence | Higher is better |
| **Scalability** | Growth capacity | Higher is better |
| **Complexity** | Implementation difficulty | Lower is better |

All metrics normalized to **0-100 scale** for easy comparison.

---

## 🎨 Features

### 🔄 Self-Improvement Loop

MetaMind automatically critiques and improves designs:

1. **Reflection Agent** analyzes the design and assigns confidence score
2. If confidence < 0.85, **Iteration Agent** applies improvements
3. Process repeats until confidence ≥ 0.85 or max iterations reached
4. All versions stored for comparison

### 💻 Production-Ready Code Generation

Generate complete applications with:
- ✅ FastAPI backend with ML models
- ✅ Docker Compose with PostgreSQL, Redis, Prometheus, Grafana
- ✅ Multi-stage Dockerfile for optimization
- ✅ Comprehensive README with deployment guide
- ✅ Environment configuration templates
- ✅ Health checks and monitoring

### 🎯 Domain-Adaptive Optimization

Weights automatically tuned based on domain:

**Healthcare:** Prioritizes Risk (30%) + Compliance (30%)  
**Finance:** Balances Risk (25%) + Compliance (25%) + Latency (20%)  
**E-commerce:** Optimizes Latency (25%) + Scalability (25%)  

---

## 📖 Documentation

- **[Implementation Guide](IMPLEMENTATION.md)** - Complete technical documentation (1000+ lines)
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when running)

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# LLM Provider (choose one)
GROK_API_KEY=your_grok_api_key_here
# OR
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3

# Database
DB_PATH=./metamind.db

# Server
PORT=8000
LOG_LEVEL=INFO

# CORS (for production)
CORS_ORIGINS=https://yourdomain.com
```

### Domain Weights Customization

Edit [`backend/agents/domain_weight_tuning_agent.py`](backend/agents/domain_weight_tuning_agent.py):

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

## 🐳 Docker Deployment

### Development

```bash
docker-compose up -d
docker-compose logs -f
```

### Production

```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down
```

---

## ☸️ Kubernetes Deployment

MetaMind is fully ready for Kubernetes deployment with production-grade manifests!

### Quick Start (Minikube)

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Configure your API key
nano k8s/secret.yaml

# Deploy everything
cd k8s
./deploy.sh

# Access the application
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
```

Then visit: **http://localhost:8080**

### Documentation

- **[⚡ Quick Start Guide](k8s/QUICKSTART.md)** - Get started in 5 minutes!
- **[📖 Complete Deployment Guide](k8s/README.md)** - Detailed instructions
- **[🚀 Kubernetes Overview](KUBERNETES_DEPLOYMENT.md)** - Architecture and best practices

### What's Included

✅ **Production-ready manifests** for all services
✅ **Automated deployment script** with health checks
✅ **ConfigMaps and Secrets** for configuration
✅ **PersistentVolume** for database storage
✅ **Ingress** configuration for external access
✅ **Resource limits** and health probes
✅ **Horizontal scaling** support
✅ **Complete documentation** for beginners

### Cloud Deployment

Works with:
- **Google Kubernetes Engine (GKE)**
- **Amazon Elastic Kubernetes Service (EKS)**
- **Azure Kubernetes Service (AKS)**
- **DigitalOcean Kubernetes**
- **Any Kubernetes 1.19+ cluster**

---

## 📊 Performance

- **Design Generation**: 2-5 minutes per architecture
- **Candidate Evaluation**: 20-40 seconds per candidate
- **Iteration Cycle**: 1-2 minutes per improvement
- **API Response Time**: <100ms (excluding LLM calls)
- **Frontend Load Time**: <2 seconds
- **Demo Mode**: Instant results (<1 second)

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain** & **LangGraph** - LLM orchestration framework
- **FastAPI** - Modern Python web framework
- **React** & **Vite** - Frontend framework and build tool
- **Monaco Editor** - VS Code's editor for the web
- **Grok** / **Ollama** - LLM providers

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/metamind/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/metamind/discussions)
- **Email**: support@metamind.ai

---

## 🗺️ Roadmap

- [x] Core multi-agent system with 11 specialized agents
- [x] Deterministic scoring engine with 6 metrics
- [x] Reflection and iteration loop
- [x] FastAPI backend with 10 REST endpoints
- [x] Modern React frontend with Vite
- [x] Monaco Editor integration
- [x] Demo mode with instant results
- [x] Production-ready code generation
- [x] Docker deployment
- [x] Kubernetes support
- [ ] Authentication & authorization
- [ ] PostgreSQL support
- [ ] Redis caching
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] CI/CD pipeline
- [ ] More architecture templates
- [ ] Custom domain support
- [ ] API rate limiting

---

## 📈 Project Stats

- **Lines of Code**: 15,000+
- **Files**: 100+
- **Agents**: 11
- **API Endpoints**: 10
- **Architecture Templates**: 6
- **Evaluation Metrics**: 6
- **Documentation**: 3,000+ lines

---

**Built with ❤️ by the MetaMind Team**

**⭐ Star us on GitHub if you find this useful!**

---

## 🎉 Quick Links

- [🚀 Quick Start](#-quick-start)
- [📖 Documentation](IMPLEMENTATION.md)
- [🐳 Docker Deployment](#-docker-deployment)
- [🤝 Contributing](CONTRIBUTING.md)
- [📝 License](LICENSE)