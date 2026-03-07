#!/bin/bash

# MetaMind Kubernetes Deployment Script
# This script helps you deploy MetaMind to Kubernetes step by step

set -e

echo "🚀 MetaMind Kubernetes Deployment Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed. Please install kubectl first."
    echo "Visit: https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

print_info "kubectl is installed ✓"

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    print_error "Cannot connect to Kubernetes cluster."
    echo "Please ensure your cluster is running and kubectl is configured correctly."
    exit 1
fi

print_info "Kubernetes cluster is accessible ✓"
echo ""

# Step 1: Build Docker images
echo "📦 Step 1: Building Docker Images"
echo "=================================="
print_warning "Make sure you have Docker installed and running."
read -p "Do you want to build Docker images? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Building backend image..."
    docker build -t metamind-backend:latest -f ../Dockerfile.backend ..
    
    print_info "Building frontend-react image..."
    docker build -t metamind-frontend-react:latest -f ../frontend-react/Dockerfile ../frontend-react
    
    print_info "Building frontend-streamlit image..."
    docker build -t metamind-frontend-streamlit:latest -f ../Dockerfile.frontend ..
    
    print_info "Docker images built successfully ✓"
else
    print_warning "Skipping Docker image build. Make sure images are available."
fi
echo ""

# Step 2: Configure secrets
echo "🔐 Step 2: Configure API Keys"
echo "=============================="
print_warning "You need to configure your API keys before deployment."
echo ""
echo "Please edit k8s/secret.yaml and replace 'your-groq-api-key-here' with your actual API key."
echo "You can get a free API key from: https://console.groq.com/"
echo ""
read -p "Have you configured your API keys in k8s/secret.yaml? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_error "Please configure your API keys first, then run this script again."
    exit 1
fi
echo ""

# Step 3: Create namespace
echo "📁 Step 3: Creating Namespace"
echo "=============================="
print_info "Creating metamind namespace..."
kubectl apply -f namespace.yaml
print_info "Namespace created ✓"
echo ""

# Step 4: Create ConfigMap and Secrets
echo "⚙️  Step 4: Creating ConfigMap and Secrets"
echo "=========================================="
print_info "Creating ConfigMap..."
kubectl apply -f configmap.yaml

print_info "Creating Secrets..."
kubectl apply -f secret.yaml
print_info "ConfigMap and Secrets created ✓"
echo ""

# Step 5: Create PersistentVolume
echo "💾 Step 5: Creating Persistent Storage"
echo "======================================="
print_info "Creating PersistentVolume and PersistentVolumeClaim..."
kubectl apply -f persistentvolume.yaml
print_info "Storage created ✓"
echo ""

# Step 6: Deploy applications
echo "🚢 Step 6: Deploying Applications"
echo "=================================="
print_info "Deploying backend..."
kubectl apply -f backend-deployment.yaml

print_info "Deploying frontend-react..."
kubectl apply -f frontend-react-deployment.yaml

print_info "Deploying frontend-streamlit..."
kubectl apply -f frontend-streamlit-deployment.yaml
print_info "Applications deployed ✓"
echo ""

# Step 7: Create services
echo "🌐 Step 7: Creating Services"
echo "============================="
print_info "Creating services..."
kubectl apply -f services.yaml
print_info "Services created ✓"
echo ""

# Step 8: Create ingress
echo "🔗 Step 8: Creating Ingress"
echo "============================"
print_warning "This requires an Ingress Controller (like nginx-ingress) to be installed."
read -p "Do you want to create the Ingress? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    kubectl apply -f ingress.yaml
    print_info "Ingress created ✓"
else
    print_warning "Skipping Ingress creation."
fi
echo ""

# Step 9: Wait for deployments
echo "⏳ Step 9: Waiting for Deployments"
echo "==================================="
print_info "Waiting for backend to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/metamind-backend -n metamind

print_info "Waiting for frontend-react to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/metamind-frontend-react -n metamind

print_info "Waiting for frontend-streamlit to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/metamind-frontend-streamlit -n metamind

print_info "All deployments are ready ✓"
echo ""

# Step 10: Display status
echo "✅ Deployment Complete!"
echo "======================="
echo ""
print_info "Checking deployment status..."
kubectl get all -n metamind
echo ""

# Display access information
echo "🌍 Access Information"
echo "====================="
echo ""
echo "To access the application, you have several options:"
echo ""
echo "1. Port Forward (Easiest for testing):"
echo "   kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80"
echo "   Then visit: http://localhost:8080"
echo ""
echo "2. Using Ingress (if configured):"
echo "   Add to /etc/hosts: <INGRESS_IP> metamind.local"
echo "   Then visit: http://metamind.local"
echo ""
echo "3. Backend API:"
echo "   kubectl port-forward -n metamind svc/metamind-backend 8000:8000"
echo "   Then visit: http://localhost:8000/docs"
echo ""
echo "4. Streamlit UI:"
echo "   kubectl port-forward -n metamind svc/metamind-frontend-streamlit 8501:8501"
echo "   Then visit: http://localhost:8501"
echo ""

print_info "Deployment completed successfully! 🎉"
echo ""
echo "Useful commands:"
echo "  - View logs: kubectl logs -n metamind -l app=metamind --tail=100 -f"
echo "  - Check status: kubectl get pods -n metamind"
echo "  - Delete deployment: kubectl delete namespace metamind"