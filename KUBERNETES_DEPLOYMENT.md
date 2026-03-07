# 🚀 MetaMind Kubernetes Deployment

This document provides a comprehensive guide for deploying MetaMind to Kubernetes.

## 📚 Documentation Structure

We've created three levels of documentation to suit your needs:

### 1. ⚡ [Quick Start Guide](k8s/QUICKSTART.md) - **START HERE!**
**Perfect for beginners** - Get MetaMind running on Kubernetes in 5 minutes!
- Simple step-by-step instructions
- Covers installation of all prerequisites
- Uses Minikube for local testing
- Minimal configuration required

👉 **[Read the Quick Start Guide](k8s/QUICKSTART.md)**

### 2. 📖 [Complete Deployment Guide](k8s/README.md)
**For detailed understanding** - Comprehensive guide covering all aspects:
- Detailed explanations of each component
- Multiple deployment options (Minikube, Docker Desktop, Cloud)
- Troubleshooting section
- Production deployment best practices
- Advanced configuration options

👉 **[Read the Complete Guide](k8s/README.md)**

### 3. 📁 Kubernetes Manifests
**For customization** - All Kubernetes YAML files in the `k8s/` directory:
- `namespace.yaml` - Namespace definition
- `configmap.yaml` - Configuration values
- `secret.yaml` - API keys and secrets
- `persistentvolume.yaml` - Storage configuration
- `backend-deployment.yaml` - Backend service
- `frontend-react-deployment.yaml` - React UI
- `frontend-streamlit-deployment.yaml` - Streamlit UI
- `services.yaml` - Service definitions
- `ingress.yaml` - Ingress configuration
- `deploy.sh` - Automated deployment script

---

## 🎯 Quick Overview

MetaMind can be deployed to Kubernetes in three ways:

### Option 1: Automated Deployment (Recommended)
```bash
cd k8s
./deploy.sh
```

### Option 2: Manual Deployment
```bash
# Configure API key
nano k8s/secret.yaml

# Deploy all components
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/persistentvolume.yaml
kubectl apply -f k8s/backend-deployment.yaml
kubectl apply -f k8s/frontend-react-deployment.yaml
kubectl apply -f k8s/frontend-streamlit-deployment.yaml
kubectl apply -f k8s/services.yaml
kubectl apply -f k8s/ingress.yaml
```

### Option 3: Using Helm (Coming Soon)
```bash
helm install metamind ./helm/metamind
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    KUBERNETES CLUSTER                    │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │              Namespace: metamind                │    │
│  │                                                 │    │
│  │  ┌──────────────┐  ┌──────────────┐           │    │
│  │  │   Backend    │  │ Frontend     │           │    │
│  │  │   (FastAPI)  │  │ (React)      │           │    │
│  │  │   2 replicas │  │ 2 replicas   │           │    │
│  │  └──────┬───────┘  └──────┬───────┘           │    │
│  │         │                  │                    │    │
│  │         └──────────┬───────┘                    │    │
│  │                    │                            │    │
│  │         ┌──────────▼───────────┐               │    │
│  │         │   Services (ClusterIP)│              │    │
│  │         └──────────┬────────────┘              │    │
│  │                    │                            │    │
│  │         ┌──────────▼────────────┐              │    │
│  │         │   Ingress (nginx)     │              │    │
│  │         └──────────┬────────────┘              │    │
│  │                    │                            │    │
│  │  ┌─────────────────▼──────────────────┐       │    │
│  │  │   PersistentVolume (Database)      │       │    │
│  │  └────────────────────────────────────┘       │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Components

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

### Frontend Streamlit Service
- **Image**: `metamind-frontend-streamlit:latest`
- **Replicas**: 1
- **Port**: 8501
- **Resources**: 256Mi-512Mi RAM, 100m-500m CPU

---

## 🔧 Configuration

### Environment Variables (ConfigMap)
- `LLM_PROVIDER`: groq
- `GROQ_MODEL`: llama-3.1-70b-versatile
- `DB_PATH`: /app/data/metamind.db
- `PORT`: 8000
- `MAX_ITERATIONS`: 5
- `CONFIDENCE_THRESHOLD`: 0.85

### Secrets
- `GROQ_API_KEY`: Your Groq API key
- Additional API keys (optional): XAI, OpenAI, Anthropic

### Storage
- **Type**: PersistentVolume
- **Size**: 5Gi
- **Access Mode**: ReadWriteOnce
- **Storage Class**: manual (for local), or cloud-specific for production

---

## 🌐 Access Methods

### 1. Port Forwarding (Development)
```bash
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
```
Access at: http://localhost:8080

### 2. Ingress (Production)
Configure DNS to point to your Ingress IP:
```
metamind.yourdomain.com → <INGRESS_IP>
```

### 3. NodePort (Alternative)
Change service type to NodePort and access via node IP:
```bash
kubectl get nodes -o wide
```

---

## 📊 Monitoring

### View Logs
```bash
# All pods
kubectl logs -n metamind -l app=metamind --tail=100 -f

# Specific service
kubectl logs -n metamind -l component=backend --tail=50 -f
```

### Check Status
```bash
# All resources
kubectl get all -n metamind

# Pod status
kubectl get pods -n metamind -w

# Resource usage
kubectl top pods -n metamind
```

### Health Checks
```bash
# Backend health
kubectl port-forward -n metamind svc/metamind-backend 8000:8000
curl http://localhost:8000/health

# Frontend health
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
curl http://localhost:8080
```

---

## 🔄 Updates and Rollbacks

### Update Deployment
```bash
# Update image
kubectl set image deployment/metamind-backend backend=metamind-backend:v2 -n metamind

# Check rollout status
kubectl rollout status deployment/metamind-backend -n metamind
```

### Rollback
```bash
# Rollback to previous version
kubectl rollout undo deployment/metamind-backend -n metamind

# Rollback to specific revision
kubectl rollout undo deployment/metamind-backend --to-revision=2 -n metamind
```

### Scale
```bash
# Scale up
kubectl scale deployment metamind-backend --replicas=5 -n metamind

# Scale down
kubectl scale deployment metamind-backend --replicas=1 -n metamind
```

---

## 🏭 Production Considerations

### 1. High Availability
- Use at least 3 replicas for critical services
- Deploy across multiple availability zones
- Configure pod anti-affinity

### 2. Security
- Use network policies to restrict traffic
- Enable RBAC
- Scan images for vulnerabilities
- Use secrets management (e.g., HashiCorp Vault)

### 3. Performance
- Configure resource requests and limits
- Use horizontal pod autoscaling
- Enable cluster autoscaling
- Use CDN for static assets

### 4. Monitoring
- Deploy Prometheus and Grafana
- Set up alerting
- Configure log aggregation (ELK/EFK stack)
- Use distributed tracing (Jaeger)

### 5. Backup
- Regular database backups
- Backup Kubernetes manifests
- Test disaster recovery procedures

---

## 🧹 Cleanup

### Remove Deployment
```bash
# Delete all resources
kubectl delete namespace metamind

# Or delete individually
kubectl delete -f k8s/
```

### Stop Minikube
```bash
minikube stop
minikube delete
```

---

## 📚 Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [MetaMind GitHub Repository](https://github.com/yourusername/metamind)

---

## 🆘 Support

For issues or questions:
1. Check the [Troubleshooting Guide](k8s/README.md#troubleshooting)
2. View logs: `kubectl logs -n metamind -l app=metamind --tail=100`
3. Open an issue on GitHub

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by the MetaMind Team**

**⭐ Star us on GitHub if you find this useful!**