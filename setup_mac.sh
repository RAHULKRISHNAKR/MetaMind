#!/bin/bash

# ============================================
# MetaMind - Mac Setup Script
# ============================================
# Automated setup for users who have already forked and cloned the repo
# This script will install dependencies, configure environment, and start all services

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Emoji for better UX
CHECK="✅"
CROSS="❌"
WARN="⚠️"
INFO="ℹ️"
ROCKET="🚀"
GEAR="⚙️"
PACKAGE="📦"
DOCKER="🐳"
BROWSER="🌐"

# ============================================
# Helper Functions
# ============================================

print_header() {
    echo ""
    echo -e "${BOLD}${CYAN}================================${NC}"
    echo -e "${BOLD}${CYAN}$1${NC}"
    echo -e "${BOLD}${CYAN}================================${NC}"
    echo ""
}

print_step() {
    echo -e "${BLUE}${BOLD}$1${NC}"
}

print_success() {
    echo -e "${GREEN}${CHECK} $1${NC}"
}

print_error() {
    echo -e "${RED}${CROSS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${WARN} $1${NC}"
}

print_info() {
    echo -e "${CYAN}${INFO} $1${NC}"
}

# ============================================
# Banner
# ============================================

clear
echo -e "${MAGENTA}${BOLD}"
cat << "EOF"
╔═══════════════════════════════════════════╗
║                                           ║
║           🧠 MetaMind Setup               ║
║     Autonomous AI Pipeline Designer       ║
║                                           ║
╚═══════════════════════════════════════════╝
EOF
echo -e "${NC}"

print_info "This script will set up MetaMind on your Mac"
print_info "Estimated time: 5-10 minutes"
echo ""

# ============================================
# Step 1: Verify Directory
# ============================================

print_header "${GEAR} Step 1: Verifying Directory"

if [ ! -f "docker-compose.yml" ] || [ ! -f "README.md" ]; then
    print_error "Not in MetaMind root directory!"
    print_info "Please run this script from the MetaMind project root"
    exit 1
fi

print_success "Running from correct directory"

# ============================================
# Step 2: Check and Install Prerequisites
# ============================================

print_header "${GEAR} Step 2: Installing Prerequisites"

# Check if Homebrew is installed
print_step "Checking Homebrew..."
if ! command -v brew &> /dev/null; then
    print_warning "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ $(uname -m) == 'arm64' ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    print_success "Homebrew installed"
else
    print_success "Homebrew already installed"
fi

# Install Docker Desktop
print_step "Checking Docker..."
if ! command -v docker &> /dev/null; then
    print_warning "Docker not found. Installing Docker Desktop..."
    brew install --cask docker
    print_success "Docker Desktop installed"
    print_info "Starting Docker Desktop..."
    open -a Docker
    print_warning "Waiting for Docker to start (this may take 30-60 seconds)..."
    
    # Wait for Docker to start
    for i in {1..60}; do
        if docker info &> /dev/null 2>&1; then
            print_success "Docker is running"
            break
        fi
        if [ $i -eq 60 ]; then
            print_error "Docker failed to start. Please start Docker Desktop manually and run this script again."
            exit 1
        fi
        sleep 2
    done
else
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    print_success "Docker installed: $DOCKER_VERSION"
    
    # Check if Docker is running
    if ! docker info &> /dev/null 2>&1; then
        print_warning "Docker is not running. Starting Docker Desktop..."
        open -a Docker
        print_info "Waiting for Docker to start..."
        
        for i in {1..60}; do
            if docker info &> /dev/null 2>&1; then
                print_success "Docker is running"
                break
            fi
            if [ $i -eq 60 ]; then
                print_error "Docker failed to start. Please start Docker Desktop manually and run this script again."
                exit 1
            fi
            sleep 2
        done
    else
        print_success "Docker daemon is running"
    fi
fi

# Check Docker Compose
print_step "Checking Docker Compose..."
if docker compose version &> /dev/null; then
    COMPOSE_VERSION=$(docker compose version | awk '{print $4}')
    print_success "Docker Compose installed: $COMPOSE_VERSION"
else
    print_warning "Docker Compose not found (should come with Docker Desktop)"
fi

# Install Python
print_step "Checking Python..."
if ! command -v python3 &> /dev/null; then
    print_warning "Python not found. Installing Python 3.11..."
    brew install python@3.11
    print_success "Python installed"
else
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    print_success "Python installed: $PYTHON_VERSION"
    
    # Check Python version
    PYTHON_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
    PYTHON_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]; then
        print_warning "Python 3.11+ recommended. Installing Python 3.11..."
        brew install python@3.11
    else
        print_success "Python version is 3.11+"
    fi
fi

# Install Node.js
print_step "Checking Node.js..."
if ! command -v node &> /dev/null; then
    print_warning "Node.js not found. Installing Node.js..."
    brew install node
    print_success "Node.js installed"
else
    NODE_VERSION=$(node --version)
    print_success "Node.js installed: $NODE_VERSION"
    
    # Check Node version
    NODE_MAJOR=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_MAJOR" -lt 18 ]; then
        print_warning "Node.js 18+ recommended. Upgrading Node.js..."
        brew upgrade node
    else
        print_success "Node.js version is 18+"
    fi
fi

# Check npm
print_step "Checking npm..."
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    print_success "npm installed: $NPM_VERSION"
else
    print_error "npm not found (should come with Node.js)"
    exit 1
fi

# Install kubectl
print_step "Checking kubectl..."
if ! command -v kubectl &> /dev/null; then
    print_warning "kubectl not found. Installing kubectl..."
    brew install kubectl
    print_success "kubectl installed"
else
    print_success "kubectl already installed"
fi

# Install minikube
print_step "Checking minikube..."
if ! command -v minikube &> /dev/null; then
    print_warning "minikube not found. Installing minikube..."
    brew install minikube
    print_success "minikube installed"
else
    print_success "minikube already installed"
fi

print_success "All prerequisites installed!"

# ============================================
# Step 3: Check Port Availability
# ============================================

print_header "${GEAR} Step 3: Checking Port Availability"

check_port() {
    local port=$1
    local service=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port $port is in use ($service)"
        echo -e "   ${YELLOW}Run: kill -9 \$(lsof -ti:$port)${NC}"
        return 1
    else
        print_success "Port $port is available ($service)"
        return 0
    fi
}

PORTS_OK=1
check_port 8000 "Backend API" || PORTS_OK=0
check_port 8501 "Streamlit Frontend" || PORTS_OK=0
check_port 5173 "React Frontend Dev" || PORTS_OK=0
check_port 80 "React Frontend Prod" || PORTS_OK=0

if [ $PORTS_OK -eq 0 ]; then
    echo ""
    read -p "$(echo -e ${YELLOW}Continue anyway? [y/N]: ${NC})" -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Setup cancelled. Free the ports and run again."
        exit 1
    fi
fi

# ============================================
# Step 4: Environment Configuration
# ============================================

print_header "${GEAR} Step 4: Environment Configuration"

if [ -f ".env" ]; then
    print_warning ".env file already exists"
    read -p "$(echo -e ${YELLOW}Overwrite with new configuration? [y/N]: ${NC})" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm .env
        print_info "Removed existing .env file"
    else
        print_info "Keeping existing .env file"
        ENV_EXISTS=1
    fi
fi

if [ ! -f ".env" ]; then
    print_step "Creating .env file from template..."
    cp .env.example .env
    print_success "Created .env file"
    
    echo ""
    print_info "MetaMind supports multiple LLM providers:"
    echo -e "  ${GREEN}1. Groq${NC} - Fast, free tier available (Recommended)"
    echo -e "  ${CYAN}2. Ollama${NC} - Local, completely free"
    echo -e "  ${BLUE}3. xAI Grok${NC} - Fast, \$5/1M tokens"
    echo -e "  ${MAGENTA}4. OpenAI${NC} - \$30/1M tokens"
    echo ""
    
    read -p "$(echo -e ${CYAN}Enter your Groq API key [or press Enter to skip]: ${NC})" GROQ_KEY
    
    if [ ! -z "$GROQ_KEY" ]; then
        # Update .env file with the API key
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/your-groq-api-key-here/$GROQ_KEY/" .env
        else
            sed -i "s/your-groq-api-key-here/$GROQ_KEY/" .env
        fi
        print_success "Groq API key configured"
    else
        print_warning "No API key provided"
        print_info "Get free API key: https://console.groq.com/"
        print_info "You can add it later by editing .env file"
    fi
else
    print_success "Using existing .env configuration"
fi

# ============================================
# Step 5: Install Backend Dependencies
# ============================================

print_header "${PACKAGE} Step 5: Installing Backend Dependencies"

print_step "Installing Python packages..."
print_info "This may take a few minutes..."

cd backend
if pip3 install -r requirements.txt --quiet; then
    print_success "Backend dependencies installed"
else
    print_error "Failed to install backend dependencies"
    print_info "Try: pip3 install -r backend/requirements.txt"
    exit 1
fi
cd ..

# ============================================
# Step 6: Install Frontend Dependencies
# ============================================

print_header "${PACKAGE} Step 6: Installing Frontend Dependencies"

print_step "Installing Node.js packages for React frontend..."
print_info "This may take a few minutes..."

cd frontend-react
if npm install --silent; then
    print_success "Frontend dependencies installed"
else
    print_error "Failed to install frontend dependencies"
    print_info "Try: cd frontend-react && npm install"
    exit 1
fi
cd ..

# ============================================
# Step 7: Kubernetes/Minikube Deployment
# ============================================

print_header "${ROCKET} Step 7: Kubernetes Setup"

print_info "Using Kubernetes/Minikube for deployment (production-like environment)"
echo ""

DEPLOY_CHOICE="1"
# Start minikube
print_step "Starting minikube..."
if minikube status 2>/dev/null | grep -q "Running"; then
    print_success "minikube already running"
else
    print_info "Starting minikube with 4 CPUs and 8GB RAM..."
    print_warning "This may take 2-3 minutes on first run..."
    if minikube start --cpus=4 --memory=8192; then
        print_success "minikube started"
    else
        print_error "Failed to start minikube"
        exit 1
    fi
fi

# Switch to Minikube's Docker
print_step "Switching to Minikube's Docker environment..."
eval $(minikube docker-env)
print_success "Using Minikube's Docker daemon"

# Verify Docker context
DOCKER_NAME=$(docker info 2>/dev/null | grep "Name:" | awk '{print $2}')
if [ "$DOCKER_NAME" = "minikube" ]; then
    print_success "Verified: Using Minikube Docker"
else
    print_warning "Docker context may not be set to Minikube (continuing anyway)"
fi

# Build images
print_header "${DOCKER} Step 8: Building Docker Images"

print_step "Building backend image..."
print_info "This may take 5-10 minutes on first run..."
if docker build -t metamind-backend:latest -f Dockerfile.backend . 2>&1 | grep -v "^#"; then
    print_success "Backend image built"
else
    print_error "Failed to build backend image"
    exit 1
fi

print_step "Building React frontend image..."
if docker build -t metamind-frontend-react:latest -f frontend-react/Dockerfile ./frontend-react 2>&1 | grep -v "^#"; then
    print_success "React frontend image built"
else
    print_error "Failed to build React frontend image"
    exit 1
fi

print_step "Building Streamlit frontend image..."
if docker build -t metamind-frontend-streamlit:latest -f Dockerfile.frontend . 2>&1 | grep -v "^#"; then
    print_success "Streamlit frontend image built"
else
    print_error "Failed to build Streamlit frontend image"
    exit 1
fi

# Deploy to Kubernetes
print_header "${ROCKET} Step 9: Deploying to Kubernetes"

print_step "Deploying MetaMind to Kubernetes..."
cd k8s

# Create namespace
print_info "Creating namespace..."
kubectl apply -f namespace.yaml 2>/dev/null || true

# Create ConfigMap and Secrets
print_info "Creating ConfigMap and Secrets..."
kubectl apply -f configmap.yaml 2>/dev/null || true
kubectl apply -f secret.yaml 2>/dev/null || true

# Create PersistentVolume
print_info "Creating storage..."
kubectl apply -f persistentvolume.yaml 2>/dev/null || true

# Deploy applications
print_info "Deploying backend..."
kubectl apply -f backend-deployment.yaml 2>/dev/null || true

print_info "Deploying React frontend..."
kubectl apply -f frontend-react-deployment.yaml 2>/dev/null || true

print_info "Deploying Streamlit frontend..."
kubectl apply -f frontend-streamlit-deployment.yaml 2>/dev/null || true

# Create services
print_info "Creating services..."
kubectl apply -f services.yaml 2>/dev/null || true

print_success "Kubernetes deployment complete"

# Wait for deployments
print_info "Waiting for deployments to be ready (this may take 2-3 minutes)..."
kubectl wait --for=condition=available --timeout=300s deployment/metamind-backend -n metamind 2>/dev/null || print_warning "Backend deployment timeout"
kubectl wait --for=condition=available --timeout=300s deployment/metamind-frontend-react -n metamind 2>/dev/null || print_warning "React frontend timeout"
kubectl wait --for=condition=available --timeout=300s deployment/metamind-frontend-streamlit -n metamind 2>/dev/null || print_warning "Streamlit frontend timeout"

cd ..

# Setup port forwarding
print_header "${BROWSER} Step 10: Setting Up Access"

print_step "Setting up port forwarding..."
print_info "Starting port-forward in background..."

# Kill any existing port-forwards
pkill -f "kubectl port-forward" 2>/dev/null || true
sleep 2

# Start port forwarding in background
kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80 > /dev/null 2>&1 &
PF_PID=$!

print_success "Port forwarding started (PID: $PF_PID)"
print_info "Waiting for service to be ready..."
sleep 5

# Health check
for i in {1..30}; do
    if curl -s http://localhost:8080 > /dev/null 2>&1; then
        print_success "React frontend is ready at http://localhost:8080"
        break
    fi
    if [ $i -eq 30 ]; then
        print_warning "Frontend timeout - service may need more time to start"
        print_info "You can manually check: kubectl get pods -n metamind"
    fi
    sleep 2
done

FRONTEND_URL="http://localhost:8080"
BACKEND_URL="http://localhost:8000"
STREAMLIT_URL="http://localhost:8501"

# Save port-forward PID for cleanup
echo $PF_PID > .port-forward.pid

# ============================================
# Final Step: Success & Next Steps
# ============================================

print_header "${ROCKET} Setup Complete!"

echo -e "${GREEN}${BOLD}"
cat << "EOF"
╔═══════════════════════════════════════════╗
║                                           ║
║     🎉 MetaMind is Ready to Use! 🎉      ║
║                                           ║
╚═══════════════════════════════════════════╝
EOF
echo -e "${NC}"

echo -e "${BOLD}${CYAN}📍 Access URLs:${NC}"
echo -e "  ${GREEN}React Frontend:${NC}      $FRONTEND_URL"
echo -e "  ${BLUE}Streamlit Frontend:${NC}  $STREAMLIT_URL"
echo -e "  ${MAGENTA}API Documentation:${NC}   $BACKEND_URL/docs"
echo -e "  ${YELLOW}API Health:${NC}          $BACKEND_URL/health"
echo ""

echo -e "${BOLD}${CYAN}🎯 Quick Start:${NC}"
echo -e "  1. Open ${GREEN}$FRONTEND_URL${NC} in your browser"
echo -e "  2. Click ${BOLD}'Try Demo'${NC} for instant results"
echo -e "  3. Or create a custom AI pipeline design"
echo ""

echo -e "${BOLD}${CYAN}📚 Documentation:${NC}"
echo -e "  • Getting Started:  ${BLUE}docs/GETTING_STARTED.md${NC}"
echo -e "  • Architecture:     ${BLUE}docs/ARCHITECTURE.md${NC}"
echo -e "  • API Reference:    ${BLUE}docs/API_REFERENCE.md${NC}"
echo -e "  • Troubleshooting:  ${BLUE}docs/TROUBLESHOOTING.md${NC}"
echo ""

echo -e "${BOLD}${CYAN}🛠️  Kubernetes Commands:${NC}"
echo -e "  • View pods:        ${YELLOW}kubectl get pods -n metamind${NC}"
echo -e "  • View logs:        ${YELLOW}kubectl logs -n metamind -l app=metamind -f${NC}"
echo -e "  • Port forward:     ${YELLOW}kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80${NC}"
echo -e "  • Stop minikube:    ${YELLOW}minikube stop${NC}"
echo -e "  • Delete all:       ${YELLOW}kubectl delete namespace metamind${NC}"
echo ""
echo -e "${BOLD}${CYAN}📝 Additional Access Options:${NC}"
echo -e "  • Backend API:      ${YELLOW}kubectl port-forward -n metamind svc/metamind-backend 8000:8000${NC}"
echo -e "  • Streamlit UI:     ${YELLOW}kubectl port-forward -n metamind svc/metamind-frontend-streamlit 8501:8501${NC}"
echo ""
print_info "Port forwarding is running in background (PID: $PF_PID)"
print_warning "To stop port forwarding: kill $PF_PID"

echo ""

# Open browser automatically
print_step "Opening browser..."
sleep 2

if command -v open &> /dev/null; then
    open $FRONTEND_URL
    print_success "Browser opened"
elif command -v xdg-open &> /dev/null; then
    xdg-open $FRONTEND_URL
    print_success "Browser opened"
else
    print_info "Please open $FRONTEND_URL in your browser"
fi

echo ""
echo -e "${GREEN}${BOLD}Happy building with MetaMind! 🚀${NC}"
echo ""

print_info "Note: Keep this terminal open to maintain port forwarding"
print_info "Press Ctrl+C to stop port forwarding when done"
echo ""
print_warning "If port forwarding stops, run: kubectl port-forward -n metamind svc/metamind-frontend-react 8080:80"
