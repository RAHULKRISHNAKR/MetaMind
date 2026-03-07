# 🚀 MetaMind Kubernetes Deployment Guide

This guide will help you deploy MetaMind to Kubernetes step by step, even if you're a complete beginner.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Accessing the Application](#accessing-the-application)
5. [Troubleshooting](#troubleshooting)
6. [Production Deployment](#production-deployment)
7. [Useful Commands](#useful-commands)

---

## 🎯 Prerequisites

Before you begin, you need to install the following tools:

### 1. Docker
Docker is used to build container images.

**Installation:**
- **macOS**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Windows**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Follow [official guide](https://docs.docker.com/engine/install/)

**Verify installation:**
```bash
docker --version
```

### 2. Kubernetes Cluster

You need a Kubernetes cluster. For beginners, we recommend **Minikube** for local testing.

#### Option A: Minikube (Recommended for Beginners)

**Installation:**
- **macOS**: `brew install minikube`
- **Windows**: Download from [Minikube releases](https://minikube.sigs.k8s.io/docs/start/)
- **Linux**: 
  ```bash
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo install minikube-linux-amd64 /usr/local/bin/minikube
  ```

**Start Minikube:**
```bash
minikube start --cpus=4 --memory=8192
```

**Verify:**
```bash
minikube status
```

#### Option B: Docker Desktop Kubernetes

If you have Docker Desktop, you can enable Kubernetes:
1. Open Docker Desktop
2. Go to Settings → Kubernetes
3. Check "Enable Kubernetes"
4. Click "Apply & Restart"

#### Option C: Cloud Providers (Production)

- **Google Cloud (GKE)**: [Setup Guide](https://cloud.google.com/kubernetes-engine/docs/quickstart)
- **AWS (EKS)**: [Setup Guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html)
- **Azure (AKS)**: [Setup Guide](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough)

### 3. kubectl

kubectl is the Kubernetes command-line tool.

**Installation:**
- **macOS**: `brew install kubectl`
- **Windows**: Download from [Kubernetes releases](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)
- **Linux**: 
  ```bash
  curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
  sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
  ```

**Verify:**
```bash
kubectl version --client
kubectl cluster-info
```

### 4. API Keys

You need an API key from one of these LLM providers:
- **Groq** (Recommended - Free tier): [Get API Key](https://console.groq.com/)
- **xAI Grok**: [Get API Key](https://console.x.ai/)
- **OpenAI**: [Get API Key](https://platform.openai.com/)

---

## 🚀 Quick Start

### Step 1: Configure API Keys

Edit the secret file with your API key:

```bash
# Open the secret file
nano k8s/secret.yaml

# Replace 'your-groq-api-key-here' with your actual API key
# Save and exit (Ctrl+X, then Y, then Enter)
```

### Step 2: Run the Deployment Script

```bash
cd k8s
./deploy.sh
```

The script will:
1. ✅ Check prerequisites
2. 🏗️ Build Docker images
3. 🔐 Create secrets and config
4. 📦 Deploy all services
5. ⏳ Wait for everything to be ready
6. 📊 Show you how to access the app

### Step 3: Access the Application

After deployment, use port forwarding to access the app:

```bash
# Access React Frontend (Main UI)
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
```

Then open your browser to: **http://localhost:8080**

---

## 📖 Detailed Setup

If you prefer to deploy manually or want to understand each step:

### Step 1: Build Docker Images

```bash
# Navigate to project root
cd /path/to/MetaMind

# Build backend image
docker build -t metamind-backend:latest -f Dockerfile.backend .

# Build React frontend image
docker build -t metamind-frontend-react:latest -f frontend-react/Dockerfile ./frontend-react

# Build Streamlit frontend image
docker build -t metamind-frontend-streamlit:latest -f Dockerfile.frontend .

# Verify images
docker images | grep metamind
```

### Step 2: Configure for Minikube (if using Minikube)

If you're using Minikube, you need to load images into Minikube:

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild images in Minikube's Docker
docker build -t metamind-backend:latest -f Dockerfile.backend .
docker build -t metamind-frontend-react:latest -f frontend-react/Dockerfile ./frontend-react
docker build -t metamind-frontend-streamlit:latest -f Dockerfile.frontend .
```

### Step 3: Create Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### Step 4: Configure Secrets

Edit the secret file:
```bash
nano k8s/secret.yaml
```

Replace `your-groq-api-key-here` with your actual API key, then apply:
```bash
kubectl apply -f k8s/secret.yaml
```

### Step 5: Create ConfigMap

```bash
kubectl apply -f k8s/configmap.yaml
```

### Step 6: Create Storage

```bash
kubectl apply -f k8s/persistentvolume.yaml
```

### Step 7: Deploy Applications

```bash
# Deploy backend
kubectl apply -f k8s/backend-deployment.yaml

# Deploy React frontend
kubectl apply -f k8s/frontend-react-deployment.yaml

# Deploy Streamlit frontend
kubectl apply -f k8s/frontend-streamlit-deployment.yaml
```

### Step 8: Create Services

```bash
kubectl apply -f k8s/services.yaml
```

### Step 9: Create Ingress (Optional)

First, install NGINX Ingress Controller:

**For Minikube:**
```bash
minikube addons enable ingress
```

**For other clusters:**
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
```

Then create the ingress:
```bash
kubectl apply -f k8s/ingress.yaml
```

### Step 10: Verify Deployment

```bash
# Check all resources
kubectl get all -n metamind

# Check pod status
kubectl get pods -n metamind

# Check services
kubectl get svc -n metamind

# View logs
kubectl logs -n metamind -l app=metamind --tail=50
```

---

## 🌐 Accessing the Application

### Method 1: Port Forwarding (Easiest)

**React Frontend (Main UI):**
```bash
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
```
Visit: http://localhost:8080

**Backend API:**
```bash
kubectl port-forward -n metamind svc/metamind-backend 8000:8000
```
Visit: http://localhost:8000/docs

**Streamlit UI:**
```bash
kubectl port-forward -n metamind svc/metamind-frontend-streamlit 8501:8501
```
Visit: http://localhost:8501

### Method 2: Using Ingress

If you configured Ingress:

**For Minikube:**
```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts (Linux/Mac) or C:\Windows\System32\drivers\etc\hosts (Windows)
<MINIKUBE_IP> metamind.local
```

Then visit:
- Main UI: http://metamind.local
- API: http://metamind.local/api
- Streamlit: http://metamind.local/streamlit

**For Cloud Providers:**
```bash
# Get Ingress IP
kubectl get ingress -n metamind

# Add to your DNS or /etc/hosts
<INGRESS_IP> metamind.local
```

### Method 3: NodePort (Alternative)

Edit `k8s/services.yaml` and change service type to `NodePort`:

```yaml
spec:
  type: NodePort  # Change from ClusterIP
```

Then apply and get the port:
```bash
kubectl apply -f k8s/services.yaml
kubectl get svc -n metamind
```

**For Minikube:**
```bash
minikube service metamind-frontend-react -n metamind
```

---

## 🔧 Troubleshooting

### Pods Not Starting

Check pod status:
```bash
kubectl get pods -n metamind
kubectl describe pod <pod-name> -n metamind
```

Common issues:
- **ImagePullBackOff**: Images not available. Rebuild or check image names.
- **CrashLoopBackOff**: Check logs with `kubectl logs <pod-name> -n metamind`
- **Pending**: Check if PersistentVolume is bound

### Cannot Access Application

1. Check if pods are running:
   ```bash
   kubectl get pods -n metamind
   ```

2. Check if services are created:
   ```bash
   kubectl get svc -n metamind
   ```

3. Test backend health:
   ```bash
   kubectl port-forward -n metamind svc/metamind-backend 8000:8000
   curl http://localhost:8000/health
   ```

### API Key Issues

If you see authentication errors:
1. Verify secret is created:
   ```bash
   kubectl get secret metamind-secrets -n metamind
   ```

2. Check if API key is correct:
   ```bash
   kubectl get secret metamind-secrets -n metamind -o yaml
   ```

3. Update the secret:
   ```bash
   kubectl delete secret metamind-secrets -n metamind
   kubectl apply -f k8s/secret.yaml
   kubectl rollout restart deployment -n metamind
   ```

### Database Issues

Check PersistentVolume:
```bash
kubectl get pv
kubectl get pvc -n metamind
```

If PVC is pending, you may need to create the directory:
```bash
# For Minikube
minikube ssh
sudo mkdir -p /mnt/data/metamind
exit
```

### View Logs

```bash
# All pods
kubectl logs -n metamind -l app=metamind --tail=100 -f

# Specific pod
kubectl logs -n metamind <pod-name> -f

# Previous crashed pod
kubectl logs -n metamind <pod-name> --previous
```

---

## 🏭 Production Deployment

### 1. Use Production-Grade Storage

Replace `hostPath` with cloud storage:

**AWS EBS:**
```yaml
storageClassName: gp2
```

**GCP Persistent Disk:**
```yaml
storageClassName: standard
```

**Azure Disk:**
```yaml
storageClassName: managed-premium
```

### 2. Configure Resource Limits

Already configured in deployment files. Adjust based on your needs:
```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "2Gi"
    cpu: "1000m"
```

### 3. Enable HTTPS

Update ingress with TLS:
```yaml
spec:
  tls:
  - hosts:
    - metamind.yourdomain.com
    secretName: metamind-tls
```

Install cert-manager for automatic SSL:
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
```

### 4. Set Up Monitoring

Install Prometheus and Grafana:
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
```

### 5. Configure Autoscaling

Create HorizontalPodAutoscaler:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: metamind-backend-hpa
  namespace: metamind
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: metamind-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 6. Backup Strategy

Set up regular backups of the database:
```bash
# Create backup job
kubectl create job --from=cronjob/metamind-backup backup-$(date +%Y%m%d) -n metamind
```

---

## 📝 Useful Commands

### Deployment Management

```bash
# View all resources
kubectl get all -n metamind

# Scale deployment
kubectl scale deployment metamind-backend --replicas=3 -n metamind

# Restart deployment
kubectl rollout restart deployment metamind-backend -n metamind

# Check rollout status
kubectl rollout status deployment metamind-backend -n metamind

# Rollback deployment
kubectl rollout undo deployment metamind-backend -n metamind
```

### Debugging

```bash
# Get pod details
kubectl describe pod <pod-name> -n metamind

# Execute command in pod
kubectl exec -it <pod-name> -n metamind -- /bin/bash

# View logs
kubectl logs <pod-name> -n metamind -f

# View events
kubectl get events -n metamind --sort-by='.lastTimestamp'
```

### Resource Management

```bash
# View resource usage
kubectl top pods -n metamind
kubectl top nodes

# View resource quotas
kubectl describe resourcequota -n metamind
```

### Cleanup

```bash
# Delete specific deployment
kubectl delete deployment metamind-backend -n metamind

# Delete all resources in namespace
kubectl delete namespace metamind

# Delete everything (including namespace)
kubectl delete -f k8s/
```

---

## 🎓 Learning Resources

- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Docker Documentation](https://docs.docker.com/)

---

## 🆘 Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. View logs: `kubectl logs -n metamind -l app=metamind --tail=100`
3. Check pod status: `kubectl get pods -n metamind`
4. Open an issue on GitHub with:
   - Error messages
   - Pod status output
   - Relevant logs

---

## 📄 File Structure

```
k8s/
├── README.md                          # This file
├── deploy.sh                          # Automated deployment script
├── namespace.yaml                     # Namespace definition
├── configmap.yaml                     # Configuration values
├── secret.yaml                        # API keys (edit before deploying)
├── persistentvolume.yaml              # Storage configuration
├── backend-deployment.yaml            # Backend deployment
├── frontend-react-deployment.yaml     # React frontend deployment
├── frontend-streamlit-deployment.yaml # Streamlit frontend deployment
├── services.yaml                      # Service definitions
└── ingress.yaml                       # Ingress configuration
```

---

**🎉 Congratulations!** You've successfully deployed MetaMind to Kubernetes!

For questions or issues, please open an issue on GitHub.