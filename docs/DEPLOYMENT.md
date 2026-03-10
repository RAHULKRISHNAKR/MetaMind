# 🚀 MetaMind Deployment Guide

This guide covers deploying MetaMind to various environments: Docker, Kubernetes, and cloud platforms.

---

## 📋 Deployment Options

1. **Docker Compose** - Quick testing and development
2. **Kubernetes** - Production-grade deployment
3. **Cloud Platforms** - AWS, GCP, Azure

---

## 🐳 Docker Compose Deployment

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- Groq API key

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/metamind.git
cd metamind

# Configure environment
cp .env.example .env
nano .env  # Add your GROQ_API_KEY

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### Access Points
- **React Frontend**: http://localhost:5173
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Management Commands

```bash
# Stop services
docker-compose stop

# Restart services
docker-compose restart

# View logs
docker-compose logs -f [service_name]

# Scale services
docker-compose up -d --scale backend=3

# Remove everything
docker-compose down -v
```

---

## ☸️ Kubernetes Deployment

### Prerequisites
- Kubernetes 1.19+ cluster
- kubectl configured
- Docker for building images
- Groq API key

### Quick Start (Minikube)

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192

# Configure API key
nano k8s/secret.yaml
# Replace 'your-groq-api-key-here' with your actual key

# Deploy everything
cd k8s
./deploy.sh

# Access the application
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
# Visit: http://localhost:8080
```

### Manual Deployment

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create ConfigMap and Secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# Create PersistentVolume
kubectl apply -f k8s/persistentvolume.yaml

# Deploy services
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-react-deployment.yaml
kubectl apply -f k8s/services.yaml

# Optional: Deploy ingress
kubectl apply -f k8s/ingress.yaml
```

### Verify Deployment

```bash
# Check all resources
kubectl get all -n metamind

# Check pod status
kubectl get pods -n metamind -w

# View logs
kubectl logs -n metamind -l app=metamind --tail=100 -f

# Check health
kubectl port-forward -n metamind svc/metamind-backend 8000:8000
curl http://localhost:8000/health
```

### Kubernetes Architecture

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

### Resource Requirements

| Component | CPU Request | CPU Limit | Memory Request | Memory Limit |
|-----------|-------------|-----------|----------------|--------------|
| Backend | 250m | 1000m | 512Mi | 2Gi |
| Frontend React | 100m | 200m | 128Mi | 256Mi |
| Frontend Streamlit | 100m | 500m | 256Mi | 512Mi |

### Scaling

```bash
# Scale backend
kubectl scale deployment metamind-backend --replicas=5 -n metamind

# Scale frontend
kubectl scale deployment metamind-frontend-react --replicas=3 -n metamind

# Auto-scaling (HPA)
kubectl autoscale deployment metamind-backend \
  --cpu-percent=70 \
  --min=2 \
  --max=10 \
  -n metamind
```

### Updates and Rollbacks

```bash
# Update image
kubectl set image deployment/metamind-backend \
  backend=metamind-backend:v2 -n metamind

# Check rollout status
kubectl rollout status deployment/metamind-backend -n metamind

# Rollback to previous version
kubectl rollout undo deployment/metamind-backend -n metamind

# Rollback to specific revision
kubectl rollout undo deployment/metamind-backend \
  --to-revision=2 -n metamind
```

---

## ☁️ Cloud Platform Deployment

### AWS (EKS)

```bash
# Create EKS cluster
eksctl create cluster \
  --name metamind \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 2 \
  --nodes-max 5

# Configure kubectl
aws eks update-kubeconfig --name metamind --region us-west-2

# Deploy MetaMind
cd k8s
./deploy.sh

# Create LoadBalancer
kubectl apply -f k8s/ingress.yaml
```

### GCP (GKE)

```bash
# Create GKE cluster
gcloud container clusters create metamind \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2

# Get credentials
gcloud container clusters get-credentials metamind \
  --zone us-central1-a

# Deploy MetaMind
cd k8s
./deploy.sh

# Expose via LoadBalancer
kubectl apply -f k8s/ingress.yaml
```

### Azure (AKS)

```bash
# Create resource group
az group create --name metamind-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group metamind-rg \
  --name metamind \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3 \
  --enable-addons monitoring

# Get credentials
az aks get-credentials \
  --resource-group metamind-rg \
  --name metamind

# Deploy MetaMind
cd k8s
./deploy.sh
```

---

## 🔧 Configuration

### Environment Variables

```env
# LLM Provider
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile

# Database
DB_PATH=/app/data/metamind.db

# Server
PORT=8000
LOG_LEVEL=INFO

# Optimization
MAX_ITERATIONS=5
CONFIDENCE_THRESHOLD=0.85

# CORS
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

### Secrets Management

**Kubernetes Secrets**:
```bash
# Create secret from file
kubectl create secret generic metamind-secrets \
  --from-file=.env \
  -n metamind

# Create secret from literal
kubectl create secret generic metamind-secrets \
  --from-literal=GROQ_API_KEY=your_key_here \
  -n metamind
```

**Docker Secrets**:
```bash
# Create secret
echo "your_api_key" | docker secret create groq_api_key -

# Use in docker-compose.yml
secrets:
  groq_api_key:
    external: true
```

---

## 🌐 Ingress Configuration

### Nginx Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: metamind-ingress
  namespace: metamind
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - metamind.yourdomain.com
    secretName: metamind-tls
  rules:
  - host: metamind.yourdomain.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: metamind-backend
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: metamind-frontend-react
            port:
              number: 80
```

### SSL/TLS with cert-manager

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF
```

---

## 📊 Monitoring

### Prometheus & Grafana

```bash
# Install Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring --create-namespace

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
# Default credentials: admin / prom-operator
```

### Logging with ELK Stack

```bash
# Install Elasticsearch
helm repo add elastic https://helm.elastic.co
helm install elasticsearch elastic/elasticsearch -n logging --create-namespace

# Install Kibana
helm install kibana elastic/kibana -n logging

# Install Filebeat
helm install filebeat elastic/filebeat -n logging
```

---

## 🔐 Security Best Practices

### 1. Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind:NetworkPolicy
metadata:
  name: metamind-network-policy
  namespace: metamind
spec:
  podSelector:
    matchLabels:
      app: metamind
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: metamind
    ports:
    - protocol: TCP
      port: 8000
```

### 2. RBAC

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

### 3. Pod Security

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: metamind-backend
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
  containers:
  - name: backend
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
```

---

## 💾 Backup and Recovery

### Database Backup

```bash
# Backup SQLite database
kubectl exec -n metamind deployment/metamind-backend -- \
  sqlite3 /app/data/metamind.db .dump > backup.sql

# Restore database
kubectl exec -i -n metamind deployment/metamind-backend -- \
  sqlite3 /app/data/metamind.db < backup.sql
```

### Automated Backups

```bash
# Create CronJob for daily backups
kubectl apply -f - <<EOF
apiVersion: batch/v1
kind: CronJob
metadata:
  name: metamind-backup
  namespace: metamind
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: metamind-backend:latest
            command:
            - /bin/sh
            - -c
            - sqlite3 /app/data/metamind.db .dump > /backups/backup-\$(date +%Y%m%d).sql
            volumeMounts:
            - name: data
              mountPath: /app/data
            - name: backups
              mountPath: /backups
          restartPolicy: OnFailure
          volumes:
          - name: data
            persistentVolumeClaim:
              claimName: metamind-pvc
          - name: backups
            persistentVolumeClaim:
              claimName: metamind-backup-pvc
EOF
```

---

## 🧹 Cleanup

### Docker Compose

```bash
# Stop and remove containers
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

### Kubernetes

```bash
# Delete namespace (removes everything)
kubectl delete namespace metamind

# Or delete individually
kubectl delete -f k8s/

# Stop Minikube
minikube stop
minikube delete
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Documentation](https://helm.sh/docs/)

---

**Ready for production deployment!** 🚀