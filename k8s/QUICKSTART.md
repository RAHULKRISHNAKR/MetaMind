# ⚡ MetaMind Kubernetes Quick Start Guide

**For Complete Beginners - Get Started in 5 Minutes!**

---

## 🎯 What You'll Need

1. **Docker** - To build container images
2. **Minikube** - A local Kubernetes cluster
3. **kubectl** - Kubernetes command-line tool
4. **API Key** - Free from Groq (https://console.groq.com/)

---

## 📦 Step 1: Install Prerequisites (One-Time Setup)

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Docker Desktop
brew install --cask docker

# Install Minikube and kubectl
brew install minikube kubectl

# Start Docker Desktop from Applications folder
```

### Windows

1. Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Download and install [Minikube](https://minikube.sigs.k8s.io/docs/start/)
3. kubectl comes with Docker Desktop

### Linux

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

---

## 🚀 Step 2: Start Minikube

```bash
# Start Minikube with enough resources
minikube start --cpus=4 --memory=8192

# Verify it's running
minikube status
```

You should see:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

---

## 🔑 Step 3: Get Your API Key

1. Go to https://console.groq.com/
2. Sign up for a free account
3. Create an API key
4. Copy the key (you'll need it in the next step)

---

## ⚙️ Step 4: Configure Your API Key

```bash
# Navigate to the project root (if not already there)
cd /path/to/MetaMind

# Edit the secret file
nano k8s/secret.yaml

# Replace 'your-groq-api-key-here' with your actual API key
# Press Ctrl+X, then Y, then Enter to save
```

---

## 🎬 Step 5: Deploy MetaMind

```bash
# Navigate to the k8s directory
cd k8s

# Make the deploy script executable (if not already done)
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

The script will:
- ✅ Check if everything is installed
- 🏗️ Build Docker images (takes 5-10 minutes first time)
- 📦 Deploy all services
- ⏳ Wait for everything to be ready
- 📊 Show you how to access the app

**Just follow the prompts and answer 'y' when asked!**

---

## 🌐 Step 6: Access MetaMind

After deployment completes, open a **new terminal** and run:

```bash
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
```

Then open your browser to: **http://localhost:8080**

🎉 **You're done!** MetaMind is now running on Kubernetes!

---

## 🎮 Using MetaMind

1. Click **"Try Demo"** to see instant results
2. Or fill in the form to design your own AI architecture
3. Watch the AI agents work in real-time
4. Download the generated code

---

## 🛑 Stopping MetaMind

When you're done:

```bash
# Stop port forwarding (Ctrl+C in the terminal)

# Stop Minikube (optional - saves resources)
minikube stop

# Delete everything (if you want to start fresh)
kubectl delete namespace metamind
```

---

## 🔄 Restarting MetaMind

Next time you want to use MetaMind:

```bash
# Start Minikube
minikube start

# Port forward to access the app
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80
```

---

## 📊 Useful Commands

```bash
# Check if everything is running
kubectl get pods -n metamind

# View logs
kubectl logs -n metamind -l app=metamind --tail=50

# Restart a service
kubectl rollout restart deployment metamind-backend -n metamind

# Access backend API docs
kubectl port-forward -n metamind svc/metamind-backend 8000:8000
# Then visit: http://localhost:8000/docs

# Access Streamlit UI (alternative interface)
kubectl port-forward -n metamind svc/metamind-frontend-streamlit 8501:8501
# Then visit: http://localhost:8501
```

---

## ❓ Troubleshooting

### "Cannot connect to Kubernetes cluster"
```bash
minikube start
```

### "Pods are not starting"
```bash
# Check pod status
kubectl get pods -n metamind

# View logs
kubectl logs -n metamind <pod-name>

# Restart deployment
kubectl rollout restart deployment -n metamind
```

### "Cannot access the application"
```bash
# Make sure port-forward is running
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80

# Try a different port if 8080 is busy
kubectl port-forward -n metamind svc/metamind-frontend-react 9090:80
```

### "Images not found"
```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Rebuild images
cd ..  # Go back to project root
docker build -t metamind-backend:latest -f Dockerfile.backend .
docker build -t metamind-frontend-react:latest -f frontend-react/Dockerfile ./frontend-react
docker build -t metamind-frontend-streamlit:latest -f Dockerfile.frontend .

# Restart deployments
kubectl rollout restart deployment -n metamind
```

---

## 🎓 Next Steps

- Read the full [README.md](README.md) for advanced features
- Learn about [production deployment](README.md#production-deployment)
- Explore [Kubernetes basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)

---

## 🆘 Need Help?

- Check the detailed [README.md](README.md)
- View logs: `kubectl logs -n metamind -l app=metamind --tail=100`
- Open an issue on GitHub

---

**Happy deploying! 🚀**