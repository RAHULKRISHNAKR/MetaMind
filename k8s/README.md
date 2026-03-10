# ☸️ MetaMind Kubernetes Deployment

Complete guide for deploying MetaMind to Kubernetes.

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Kubernetes cluster (Minikube, Docker Desktop, or cloud provider)
- kubectl installed and configured
- Docker for building images
- Groq API key from [console.groq.com](https://console.groq.com/)

### Deploy Now

```bash
# 1. Configure your API key
cd k8s
nano secret.yaml
# Replace 'your-groq-api-key-here' with your actual key

# 2. Deploy everything
./deploy.sh

# 3. Access the application
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
# Visit: http://localhost:8080
```

That's it! MetaMind is now running on Kubernetes. 🎉

---

## 📖 Detailed Guide

### Step 1: Prepare Your Cluster

**Option A: Minikube (Local Testing)**
```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Enable ingress addon (optional)
minikube addons enable ingress

# Verify cluster
kubectl cluster-info
```

**Option B: Docker Desktop (Local Testing)**
```bash
# Enable Kubernetes in Docker Desktop settings
# Verify
kubectl get nodes
```

**Option C: Cloud Provider (Production)**
```bash
# AWS EKS
eksctl create cluster --name metamind --region us-west-2

# GCP GKE
gcloud container clusters create metamind --zone us-central1-a

# Azure AKS
az aks create --resource-group metamind-rg --name metamind
```

### Step 2: Configure Secrets

Edit `secret.yaml` and add your API key:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: metamind-secrets
  namespace: metamind
type: Opaque
stringData:
  GROQ_API_KEY: "your_actual_groq_api_key_here"  # Replace this!
```

### Step 3: Build Docker Images

**For Minikube** (use local images):
```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build images
docker build -t metamind-backend:latest -f ../Dockerfile.backend ..
docker build -t metamind-frontend-react:latest -f ../Dockerfile.frontend ..
```

**For Cloud** (push to registry):
```bash
# Tag images
docker tag metamind-backend:latest your-registry/metamind-backend:latest
docker tag metamind-frontend-react:latest your-registry/metamind-frontend-react:latest

# Push to registry
docker push your-registry/metamind-backend:latest
docker push your-registry/metamind-frontend-react:latest

# Update image references in deployment files
```

### Step 4: Deploy to Kubernetes

**Automated Deployment** (Recommended):
```bash
cd k8s
./deploy.sh
```

**Manual Deployment**:
```bash
# Create namespace
kubectl apply -f namespace.yaml

# Create ConfigMap and Secrets
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml

# Create PersistentVolume
kubectl apply -f persistentvolume.yaml

# Deploy services
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-react-deployment.yaml
kubectl apply -f services.yaml

# Optional: Deploy ingress
kubectl apply -f ingress.yaml
```

### Step 5: Verify Deployment

```bash
# Check all resources
kubectl get all -n metamind

# Check pod status
kubectl get pods -n metamind -w

# View logs
kubectl logs -n metamind -l app=metamind --tail=50 -f

# Check health
kubectl port-forward -n metamind svc/metamind-backend 8000:8000
curl http://localhost:8000/health
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Namespace: metamind                         │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │   Backend    │  │ Frontend     │                    │
│  │   (FastAPI)  │  │ (React)      │                    │
│  │   2 replicas │  │ 2 replicas   │                    │
│  └──────┬───────┘  └──────┬───────┘                    │
│         │                  │                             │
│         └──────────┬───────┘                             │
│                    │                                     │
│         ┌──────────▼───────────┐                        │
│         │   Services (ClusterIP)│                       │
│         └──────────┬────────────┘                       │
│                    │                                     │
│         ┌──────────▼────────────┐                       │
│         │   Ingress (nginx)     │                       │
│         └──────────┬────────────┘                       │
│                    │                                     │
│  ┌─────────────────▼──────────────────┐                │
│  │   PersistentVolume (Database)      │                │
│  └────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Components

### Backend Service
- **Image**: `metamind-backend:latest`
- **Replicas**: 2
- **Port**: 8000
- **Resources**: 512Mi-2Gi RAM, 250m-1000m CPU
- **Health Checks**: Liveness and readiness probes
- **Storage**: PersistentVolume for SQLite database

### Frontend React Service
- **Image**: `metamind-frontend-react:latest`
- **Replicas**: 2
- **Port**: 80
- **Resources**: 128Mi-256Mi RAM, 100m-200m CPU
- **Server**: Nginx

### Configuration
- **ConfigMap**: Environment variables
- **Secret**: API keys
- **PersistentVolume**: 5Gi storage for database

---

## 🌐 Accessing the Application

### Method 1: Port Forwarding (Development)

```bash
# Forward frontend
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80

# Access at: http://localhost:8080
```

### Method 2: Ingress (Production)

1. **Install Ingress Controller**:
```bash
# Nginx Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
```

2. **Apply Ingress**:
```bash
kubectl apply -f ingress.yaml
```

3. **Get Ingress IP**:
```bash
kubectl get ingress -n metamind
```

4. **Configure DNS**:
```
metamind.yourdomain.com → <INGRESS_IP>
```

### Method 3: NodePort (Alternative)

Edit `services.yaml` to use NodePort:
```yaml
spec:
  type: NodePort
  ports:
    - port: 80
      nodePort: 30080
```

Access at: `http://<NODE_IP>:30080`

---

## 🔧 Management

### Scaling

```bash
# Scale backend
kubectl scale deployment metamind-backend --replicas=5 -n metamind

# Scale frontend
kubectl scale deployment metamind-frontend-react --replicas=3 -n metamind

# Auto-scaling
kubectl autoscale deployment metamind-backend \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  -n metamind
```

### Updates

```bash
# Update image
kubectl set image deployment/metamind-backend \
  backend=metamind-backend:v2 -n metamind

# Check rollout status
kubectl rollout status deployment/metamind-backend -n metamind

# Rollback if needed
kubectl rollout undo deployment/metamind-backend -n metamind
```

### Monitoring

```bash
# View logs
kubectl logs -n metamind -l app=metamind --tail=100 -f

# Check resource usage
kubectl top pods -n metamind
kubectl top nodes

# Get events
kubectl get events -n metamind --sort-by='.lastTimestamp'
```

---

## 🔐 Security

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: metamind-network-policy
  namespace: metamind
spec:
  podSelector:
    matchLabels:
      app: metamind
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: metamind
```

### RBAC

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: metamind-role
  namespace: metamind
rules:
- apiGroups: [""]
  resources: ["pods", "services"]
  verbs: ["get", "list", "watch"]
```

---

## 💾 Backup and Recovery

### Backup Database

```bash
# Backup
kubectl exec -n metamind deployment/metamind-backend -- \
  sqlite3 /app/data/metamind.db .dump > backup.sql

# Restore
kubectl exec -i -n metamind deployment/metamind-backend -- \
  sqlite3 /app/data/metamind.db < backup.sql
```

### Automated Backups

Create a CronJob for daily backups (see `backup-cronjob.yaml` example in docs).

---

## 🧹 Cleanup

```bash
# Delete everything
kubectl delete namespace metamind

# Or delete individually
kubectl delete -f .

# Stop Minikube
minikube stop
minikube delete
```

---

## 🐛 Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n metamind

# View logs
kubectl logs -n metamind <pod-name>

# Describe pod
kubectl describe pod -n metamind <pod-name>
```

### Common Issues

1. **ImagePullBackOff**: Build images locally for Minikube
2. **CrashLoopBackOff**: Check logs for errors
3. **Pending**: Check resource availability
4. **Connection Refused**: Verify services and ports

See [Troubleshooting Guide](../docs/TROUBLESHOOTING.md) for more details.

---

## 📚 Additional Resources

- [Main Documentation](../README.md)
- [Deployment Guide](../docs/DEPLOYMENT.md)
- [Troubleshooting Guide](../docs/TROUBLESHOOTING.md)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

---

## 📝 Files in this Directory

- `namespace.yaml` - Namespace definition
- `configmap.yaml` - Configuration values
- `secret.yaml` - API keys and secrets
- `persistentvolume.yaml` - Storage configuration
- `backend-deployment.yaml` - Backend service
- `frontend-react-deployment.yaml` - React UI
- `services.yaml` - Service definitions
- `ingress.yaml` - Ingress configuration
- `deploy.sh` - Automated deployment script

---

**MetaMind is ready for Kubernetes!** ☸️