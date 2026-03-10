# 🚀 MetaMind Setup Guide for Mac

Complete setup guide for Mac users who have already forked and cloned the repository.

---

## 📋 Prerequisites

**None!** The script automatically installs everything you need:

- ✅ **Homebrew** - Package manager for Mac (auto-installed)
- ✅ **Docker Desktop** - Container platform (auto-installed)
- ✅ **Python 3.11+** - Backend runtime (auto-installed)
- ✅ **Node.js 18+** - Frontend runtime (auto-installed)
- ✅ **kubectl** - Kubernetes CLI (auto-installed)
- ✅ **minikube** - Local Kubernetes (auto-installed)

**You only need:** A Mac with internet connection!

---

## 🎯 Quick Start (One Command)

```bash
./setup_mac.sh
```

That's it! The script will **automatically**:
1. ✅ Install Homebrew (if not present)
2. ✅ Install Docker Desktop (if not present)
3. ✅ Install Python 3.11+ (if not present)
4. ✅ Install Node.js 18+ (if not present)
5. ✅ Install kubectl (if not present)
6. ✅ Install minikube (if not present)
7. ✅ Start Docker Desktop
8. ✅ Configure environment variables (prompts for Groq API key)
9. ✅ Install Python and Node.js dependencies
10. ✅ Start Minikube with 4 CPUs and 8GB RAM
11. ✅ Build all Docker images
12. ✅ Deploy to Kubernetes
13. ✅ Set up port forwarding (8080:80)
14. ✅ Open browser to http://localhost:8080

**Total time:** 10-15 minutes on first run (mostly Docker image building)

---

## 🔧 What the Script Does

The script uses **Kubernetes/Minikube** for a production-like environment:

### Step-by-Step Process:

```bash
# 1. Install all prerequisites via Homebrew
brew install docker kubectl minikube python@3.11 node

# 2. Start Docker Desktop
open -a Docker

# 3. Start Minikube with 4 CPUs and 8GB RAM
minikube start --cpus=4 --memory=8192

# 4. Switch to Minikube's Docker environment
eval $(minikube docker-env)

# 5. Build Docker images
docker build -t metamind-backend:latest -f Dockerfile.backend .
docker build -t metamind-frontend-react:latest -f frontend-react/Dockerfile ./frontend-react
docker build -t metamind-frontend-streamlit:latest -f Dockerfile.frontend .

# 6. Deploy to Kubernetes
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/persistentvolume.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-react-deployment.yaml
kubectl apply -f k8s/frontend-streamlit-deployment.yaml
kubectl apply -f k8s/services.yaml

# 7. Set up port forwarding (runs in background)
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80 &
```

### Access URLs:
- **React Frontend:** http://localhost:8080 ✅ (auto port-forwarded)
- **Backend API:** http://localhost:8000 (manual port-forward needed)
- **Streamlit UI:** http://localhost:8501 (manual port-forward needed)

---

## 🔑 API Key Configuration

The script will prompt you for a **Groq API key** (recommended):

1. Get free API key: https://console.groq.com/
2. Enter when prompted during setup
3. Or skip and add later to `.env` file

**Supported LLM Providers:**
- **Groq** - Fast, free tier available ⭐ Recommended
- **Ollama** - Local, completely free
- **xAI Grok** - Fast, $5/1M tokens
- **OpenAI** - $30/1M tokens

---

## 📊 What Gets Installed

### Backend Dependencies
```
fastapi==0.115.0
langchain==0.3.15
langgraph==0.2.60
ollama==0.5.3
langchain-openai==0.2.14
jinja2==3.1.4
```

### Frontend Dependencies
```
react@18.3.1
vite@5.4.11
monaco-editor
tailwindcss
```

---

## 🛠️ Useful Commands

### Kubernetes/Minikube

```bash
# View all pods
kubectl get pods -n metamind

# View logs
kubectl logs -n metamind -l app=metamind -f

# Port forward backend
kubectl port-forward -n metamind svc/metamind-backend 8000:8000

# Port forward Streamlit
kubectl port-forward -n metamind svc/metamind-frontend-streamlit 8501:8501

# Stop Minikube
minikube stop

# Delete deployment
kubectl delete namespace metamind

# Restart Minikube
minikube delete && minikube start --cpus=4 --memory=8192
```

### Docker Compose

```bash
# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend

# Stop all services
docker compose down

# Restart services
docker compose restart

# Rebuild and restart
docker compose up -d --build

# Remove everything (including volumes)
docker compose down -v
```

---

## 🐛 Troubleshooting

### Port Already in Use

If you see "address already in use" errors:

```bash
# Find and kill process on port 8080
kill -9 $(lsof -ti:8080)

# Or for other ports
kill -9 $(lsof -ti:8000)
kill -9 $(lsof -ti:8501)
kill -9 $(lsof -ti:5173)
```

### Docker Not Running

```bash
# Check Docker status
docker info

# Start Docker Desktop manually
open -a Docker
```

### Minikube Issues

```bash
# Check Minikube status
minikube status

# Restart Minikube
minikube stop
minikube start --cpus=4 --memory=8192

# Delete and recreate
minikube delete
minikube start --cpus=4 --memory=8192
```

### Build Failures

```bash
# Clean Docker cache
docker system prune -a

# Rebuild from scratch
docker compose build --no-cache
```

### Port Forwarding Stopped

```bash
# Restart port forwarding
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80

# Run in background
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80 &
```

---

## 📁 Project Structure

```
MetaMind/
├── setup_mac.sh              # Main setup script
├── docker-compose.yml        # Docker Compose config
├── .env                      # Environment variables (created by script)
├── backend/                  # FastAPI backend
│   ├── agents/              # 11 specialized AI agents
│   ├── api/                 # REST API endpoints
│   └── requirements.txt     # Python dependencies
├── frontend-react/          # React frontend
│   ├── src/                 # React components
│   └── package.json         # Node dependencies
├── k8s/                     # Kubernetes manifests
│   ├── deploy.sh           # K8s deployment script
│   └── *.yaml              # K8s resources
└── docs/                    # Documentation
```

---

## 🎯 Next Steps After Setup

1. **Try Demo Mode**
   - Open http://localhost:8080 (K8s) or http://localhost:5173 (Docker Compose)
   - Click "Try Demo" button
   - Select a pre-configured scenario

2. **Create Custom Pipeline**
   - Enter your business goal
   - Select domain (Healthcare, Finance, E-commerce, etc.)
   - Configure constraints
   - Let MetaMind design your AI pipeline

3. **Explore API**
   - Visit http://localhost:8000/docs
   - Try interactive API documentation
   - Test endpoints with Swagger UI

4. **Read Documentation**
   - [Getting Started](docs/GETTING_STARTED.md)
   - [Architecture](docs/ARCHITECTURE.md)
   - [API Reference](docs/API_REFERENCE.md)

---

## 🔄 Updating MetaMind

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart (Docker Compose)
docker compose down
docker compose up -d --build

# Rebuild and restart (Kubernetes)
eval $(minikube docker-env)
docker build -t metamind-backend:latest -f Dockerfile.backend .
docker build -t metamind-frontend-react:latest -f frontend-react/Dockerfile ./frontend-react
kubectl rollout restart deployment -n metamind
```

---

## 💡 Tips

- **First time setup**: Takes 5-10 minutes
- **Subsequent runs**: Takes 2-3 minutes
- **Kubernetes**: More production-like, better for learning
- **Docker Compose**: Simpler, faster for development
- **Port forwarding**: Keep terminal open when using Kubernetes
- **API keys**: Can be added later to `.env` file

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/metamind/issues)
- **Documentation**: [docs/](docs/)
- **Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

**Built with ❤️ by the MetaMind Team**

**⭐ Star us on GitHub if you find this useful!**