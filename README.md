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

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Docker and Docker Compose
- Groq API key (free at [console.groq.com](https://console.groq.com/))

### Run with Docker Compose

```bash
# Clone repository
git clone https://github.com/yourusername/metamind.git
cd metamind

# Configure API key
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Start all services
docker-compose up -d

# Access the application
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### Try Demo Mode

1. Open http://localhost:5173
2. Click **"Try Demo"** button
3. Select a pre-configured scenario:
   - 🏥 Healthcare Patient Monitoring
   - 🛒 E-commerce Recommendation Engine
4. Get instant results with production-ready code!

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[Getting Started](docs/GETTING_STARTED.md)** | Complete setup guide for local development |
| **[Architecture](docs/ARCHITECTURE.md)** | System design and agent specifications |
| **[Deployment](docs/DEPLOYMENT.md)** | Docker, Kubernetes, and cloud deployment |
| **[API Reference](docs/API_REFERENCE.md)** | REST API endpoints and usage |
| **[Development](docs/DEVELOPMENT.md)** | Contributing and development workflow |
| **[Troubleshooting](docs/TROUBLESHOOTING.md)** | Common issues and solutions |

---

## 🏗️ Architecture Overview

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
│  Groq API    │         │   SQLITE DB  │
│  (LLM)       │         │  (Versions)  │
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

## 🎯 Usage Example

### API Request
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

### Response
```json
{
  "run_id": "uuid",
  "status": "completed",
  "selected_architecture": {
    "name": "E-commerce RAG Chatbot",
    "score": 78.2,
    "metrics": {
      "cost": 95.0,
      "latency": 92.0,
      "risk": 65.0,
      "compliance": 80.0,
      "scalability": 100.0,
      "complexity": 30.0
    }
  }
}
```

---

## ☸️ Kubernetes Deployment

Deploy to production in minutes:

```bash
# Configure API key
nano k8s/secret.yaml

# Deploy everything
cd k8s
./deploy.sh

# Access the application
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
# Visit: http://localhost:8080
```

**📚 Complete Guide**: See [Deployment Documentation](docs/DEPLOYMENT.md)

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

## 📈 Performance

- **Design Generation**: 2-5 minutes per architecture
- **Candidate Evaluation**: 20-40 seconds per candidate
- **Iteration Cycle**: 1-2 minutes per improvement
- **API Response Time**: <100ms (excluding LLM calls)
- **Frontend Load Time**: <2 seconds
- **Demo Mode**: Instant results (<1 second)

---

## 🤝 Contributing

Contributions are welcome! Please read our [Development Guide](docs/DEVELOPMENT.md).

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
- **Groq** - Fast LLM inference

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/metamind/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/metamind/discussions)
- **Documentation**: [docs/](docs/)

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

---

**Built with ❤️ by the MetaMind Team**

**⭐ Star us on GitHub if you find this useful!**