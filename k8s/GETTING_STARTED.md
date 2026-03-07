# 🎯 Getting Started with MetaMind on Kubernetes

**Welcome!** This guide will help you deploy MetaMind to Kubernetes in just a few steps.

---

## 📋 What You Need

Before starting, make sure you have:

1. ✅ **Docker** installed and running
2. ✅ **Kubernetes cluster** (Minikube, Docker Desktop, or cloud)
3. ✅ **kubectl** command-line tool
4. ✅ **API Key** from Groq (free at https://console.groq.com/)

**Don't have these yet?** Follow the [Quick Start Guide](QUICKSTART.md) for installation instructions.

---

## 🚀 Three Ways to Deploy

### Option 1: Automated (Easiest) ⭐

```bash
# 1. Configure your API key (from project root)
nano k8s/secret.yaml
# Replace 'your-groq-api-key-here' with your actual key

# 2. Run the deployment script
cd k8s
./deploy.sh

# 3. Access the app
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
```

Visit: http://localhost:8080

### Option 2: Manual (Step by Step)

```bash
# 1. Configure API key (from project root)
nano k8s/secret.yaml

# 2. Build Docker images (from project root)
docker build -t metamind-backend:latest -f Dockerfile.backend .
docker build -t metamind-frontend-react:latest -f frontend-react/Dockerfile ./frontend-react
docker build -t metamind-frontend-streamlit:latest -f Dockerfile.frontend .

# 3. Deploy to Kubernetes
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/persistentvolume.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-react-deployment.yaml
kubectl apply -f k8s/frontend-streamlit-deployment.yaml
kubectl apply -f k8s/services.yaml

# 4. Wait for pods to be ready
kubectl get pods -n metamind -w

# 5. Access the app
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
```

### Option 3: Using Minikube (For Local Testing)

```bash
# 1. Start Minikube
minikube start --cpus=4 --memory=8192

# 2. Use Minikube's Docker daemon
eval $(minikube docker-env)

# 3. Build images in Minikube
docker build -t metamind-backend:latest -f Dockerfile.backend .
docker build -t metamind-frontend-react:latest -f frontend-react/Dockerfile ./frontend-react
docker build -t metamind-frontend-streamlit:latest -f Dockerfile.frontend .

# 4. Configure API key (go back to project root first)
cd ..
nano k8s/secret.yaml

# 5. Deploy
cd k8s
./deploy.sh

# 6. Access the app
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
```

---

## 🎮 Using MetaMind

Once deployed and accessible at http://localhost:8080:

### Try Demo Mode (Fastest)
1. Click **"Try Demo"** button
2. Select a scenario (Healthcare or E-commerce)
3. Get instant results with production-ready code

### Design Custom Architecture
1. Fill in the form:
   - Business goal
   - Domain (Healthcare, Finance, E-commerce, etc.)
   - Modalities (Text, Image, Audio, Video)
   - Constraints (Budget, latency, users, etc.)
2. Click **"🚀 Design Architecture"**
3. Watch AI agents work in real-time
4. View results and download code

---

## 📊 Checking Status

```bash
# View all resources
kubectl get all -n metamind

# Check pod status
kubectl get pods -n metamind

# View logs
kubectl logs -n metamind -l app=metamind --tail=50 -f

# Check specific service logs
kubectl logs -n metamind -l component=backend --tail=50 -f
```

---

## 🔧 Common Tasks

### Restart a Service
```bash
kubectl rollout restart deployment metamind-backend -n metamind
```

### Scale Up/Down
```bash
# Scale up
kubectl scale deployment metamind-backend --replicas=3 -n metamind

# Scale down
kubectl scale deployment metamind-backend --replicas=1 -n metamind
```

### Update Configuration
```bash
# Edit ConfigMap
kubectl edit configmap metamind-config -n metamind

# Restart deployments to pick up changes
kubectl rollout restart deployment -n metamind
```

### Update API Key
```bash
# Edit secret
kubectl edit secret metamind-secrets -n metamind

# Restart backend to use new key
kubectl rollout restart deployment metamind-backend -n metamind
```

---

## 🌐 Access Methods

### 1. Port Forwarding (Development)
```bash
# React Frontend (Main UI)
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80

# Backend API
kubectl port-forward -n metamind svc/metamind-backend 8000:8000

# Streamlit UI
kubectl port-forward -n metamind svc/metamind-frontend-streamlit 8501:8501
```

### 2. Ingress (Production)
```bash
# Install NGINX Ingress Controller (if not installed)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Create Ingress
kubectl apply -f k8s/ingress.yaml

# Get Ingress IP
kubectl get ingress -n metamind

# Add to /etc/hosts
echo "<INGRESS_IP> metamind.local" | sudo tee -a /etc/hosts
```

Visit: http://metamind.local

### 3. NodePort (Alternative)
Edit `k8s/services.yaml` and change service type to `NodePort`, then:
```bash
kubectl apply -f k8s/services.yaml
kubectl get svc -n metamind
```

---

## 🛑 Stopping and Cleanup

### Stop Port Forwarding
Press `Ctrl+C` in the terminal running port-forward

### Stop Minikube (if using)
```bash
minikube stop
```

### Delete Deployment
```bash
# Delete all MetaMind resources
kubectl delete namespace metamind

# Or delete individually
kubectl delete -f k8s/
```

### Delete Minikube Cluster
```bash
minikube delete
```

---

## ❓ Troubleshooting

### Pods Not Starting
```bash
# Check pod status
kubectl get pods -n metamind

# Describe pod for details
kubectl describe pod <pod-name> -n metamind

# View logs
kubectl logs <pod-name> -n metamind
```

**Common Issues:**
- **ImagePullBackOff**: Images not available. Rebuild with Minikube's Docker daemon.
- **CrashLoopBackOff**: Check logs for errors. Usually API key or configuration issue.
- **Pending**: PersistentVolume not bound. Check storage configuration.

### Cannot Access Application
```bash
# Verify pods are running
kubectl get pods -n metamind

# Verify services exist
kubectl get svc -n metamind

# Test backend health
kubectl port-forward -n metamind svc/metamind-backend 8000:8000
curl http://localhost:8000/health
```

### API Key Issues
```bash
# Verify secret exists
kubectl get secret metamind-secrets -n metamind

# Update secret
kubectl delete secret metamind-secrets -n metamind
kubectl apply -f k8s/secret.yaml
kubectl rollout restart deployment metamind-backend -n metamind
```

---

## 📚 Documentation

- **[⚡ Quick Start](QUICKSTART.md)** - 5-minute setup guide
- **[📖 Complete Guide](README.md)** - Detailed documentation
- **[🚀 Overview](../KUBERNETES_DEPLOYMENT.md)** - Architecture and best practices

---

## 🆘 Getting Help

1. Check the [Troubleshooting](#troubleshooting) section above
2. View logs: `kubectl logs -n metamind -l app=metamind --tail=100`
3. Check pod status: `kubectl describe pod <pod-name> -n metamind`
4. Open an issue on GitHub with error details

---

## 🎉 Next Steps

Once you have MetaMind running:

1. **Try the Demo** - Click "Try Demo" to see instant results
2. **Design Your Own** - Create custom AI architectures
3. **Explore the Code** - Download and examine generated code
4. **Scale Up** - Increase replicas for production use
5. **Add Monitoring** - Set up Prometheus and Grafana
6. **Enable HTTPS** - Configure TLS with cert-manager

---

**Happy deploying! 🚀**

For questions or issues, please open an issue on GitHub.