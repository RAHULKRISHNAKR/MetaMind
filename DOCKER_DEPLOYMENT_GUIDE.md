# Docker Deployment Guide - MetaMind

Complete guide for deploying MetaMind using Docker and Docker Compose.

---

## 🐳 Architecture Overview

MetaMind uses a multi-container architecture:

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                  (metamind-network)                      │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Backend    │  │  Streamlit   │  │    React     │ │
│  │   FastAPI    │  │   Frontend   │  │   Frontend   │ │
│  │   :8000      │  │   :8501      │  │    :80       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│         │                 │                  │          │
│         └─────────────────┴──────────────────┘          │
│                           │                             │
│                    ┌──────────────┐                     │
│                    │   Volume     │                     │
│                    │ metamind-data│                     │
│                    └──────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Services

### 1. Backend (FastAPI)
- **Port:** 8000
- **Container:** `metamind-backend`
- **Health Check:** `/health` endpoint
- **Volume:** `metamind-data:/app/data` (SQLite database)

### 2. Frontend - Streamlit (Legacy)
- **Port:** 8501
- **Container:** `metamind-frontend-streamlit`
- **Health Check:** `/_stcore/health` endpoint

### 3. Frontend - React (New)
- **Port:** 80
- **Container:** `metamind-frontend-react`
- **Server:** Nginx
- **Health Check:** Root endpoint

---

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB disk space

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/MetaMind.git
cd MetaMind
```

### 2. Environment Configuration

Create `.env` file in project root:

```bash
# Backend Configuration
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3
DB_PATH=/app/data/metamind.db
PORT=8000

# Grok API (if using)
GROK_API_KEY=your_grok_api_key_here
```

### 3. Build and Start All Services

```bash
# Build all containers
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Access Applications

- **React Frontend:** http://localhost/
- **Streamlit Frontend:** http://localhost:8501/
- **Backend API:** http://localhost:8000/
- **API Docs:** http://localhost:8000/docs

---

## 🔧 Individual Service Management

### Build Specific Service

```bash
# Backend only
docker-compose build backend

# React frontend only
docker-compose build frontend-react

# Streamlit frontend only
docker-compose build frontend-streamlit
```

### Start Specific Service

```bash
# Start backend
docker-compose up -d backend

# Start React frontend
docker-compose up -d frontend-react

# Start Streamlit frontend
docker-compose up -d frontend-streamlit
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop specific service
docker-compose stop frontend-react
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend-react

# Last 100 lines
docker-compose logs --tail=100 backend
```

---

## 🏗️ Build Details

### Backend Dockerfile

**Location:** `Dockerfile.backend`

**Build Stages:**
1. Base Python 3.11 image
2. Install system dependencies
3. Install Python packages
4. Copy application code
5. Set up health check

**Size:** ~500MB

### React Frontend Dockerfile

**Location:** `frontend-react/Dockerfile`

**Build Stages:**
1. **Builder Stage:** Node.js 18 Alpine
   - Install dependencies
   - Build React app with Vite
   - Output: `dist/` directory

2. **Production Stage:** Nginx Alpine
   - Copy built assets
   - Configure nginx
   - Serve static files
   - Proxy API requests to backend

**Size:** ~25MB (optimized)

### Streamlit Frontend Dockerfile

**Location:** `Dockerfile.frontend`

**Build Stages:**
1. Base Python 3.11 image
2. Install Streamlit and dependencies
3. Copy application code
4. Configure Streamlit server

**Size:** ~800MB

---

## 🔍 Health Checks

All services include health checks for monitoring:

### Backend
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### React Frontend
```yaml
healthcheck:
  test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/"]
  interval: 30s
  timeout: 3s
  retries: 3
  start_period: 5s
```

### Streamlit Frontend
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

### Check Health Status

```bash
# All services
docker-compose ps

# Specific service
docker inspect metamind-backend --format='{{.State.Health.Status}}'
```

---

## 📊 Resource Management

### View Resource Usage

```bash
# All containers
docker stats

# Specific container
docker stats metamind-backend
```

### Recommended Resources

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G

  frontend-react:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

---

## 🔐 Security Best Practices

### 1. Environment Variables

Never commit `.env` files. Use `.env.example` as template:

```bash
cp .env.example .env
# Edit .env with your values
```

### 2. Network Isolation

Services communicate via internal Docker network:

```yaml
networks:
  metamind-network:
    driver: bridge
```

### 3. Volume Permissions

Ensure proper permissions for data volume:

```bash
docker-compose exec backend chown -R 1000:1000 /app/data
```

### 4. Update Images Regularly

```bash
# Pull latest base images
docker-compose pull

# Rebuild with latest
docker-compose build --no-cache
```

---

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Check container status
docker-compose ps

# Restart service
docker-compose restart backend
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8001:8000"  # Host:Container
```

### Database Issues

```bash
# Access backend container
docker-compose exec backend bash

# Check database
ls -la /app/data/

# Reset database (WARNING: deletes data)
docker-compose down -v
docker-compose up -d
```

### Network Issues

```bash
# Recreate network
docker-compose down
docker network prune
docker-compose up -d

# Check network
docker network inspect metamind_metamind-network
```

### Build Cache Issues

```bash
# Clear build cache
docker-compose build --no-cache

# Remove all unused images
docker image prune -a
```

---

## 📈 Production Deployment

### 1. Use Production Compose File

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    image: metamind-backend:latest
    environment:
      - ENV=production
      - DEBUG=false
    restart: always

  frontend-react:
    image: metamind-frontend-react:latest
    restart: always
```

Deploy:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 2. Enable HTTPS

Use reverse proxy (Nginx/Traefik) with Let's Encrypt:

```yaml
services:
  nginx-proxy:
    image: nginxproxy/nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/tmp/docker.sock:ro
      - ./certs:/etc/nginx/certs

  frontend-react:
    environment:
      - VIRTUAL_HOST=metamind.yourdomain.com
      - LETSENCRYPT_HOST=metamind.yourdomain.com
```

### 3. Monitoring

Add monitoring stack:

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

### 4. Backup Strategy

```bash
# Backup database
docker-compose exec backend tar -czf /tmp/backup.tar.gz /app/data
docker cp metamind-backend:/tmp/backup.tar.gz ./backups/

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec backend tar -czf /tmp/backup_$DATE.tar.gz /app/data
docker cp metamind-backend:/tmp/backup_$DATE.tar.gz ./backups/
```

---

## 🔄 Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build

# Restart with new images
docker-compose up -d

# Remove old images
docker image prune
```

### Database Migration

```bash
# Backup first
docker-compose exec backend tar -czf /tmp/backup.tar.gz /app/data

# Run migrations
docker-compose exec backend python -m alembic upgrade head
```

### Rolling Updates

```bash
# Update one service at a time
docker-compose up -d --no-deps --build backend
docker-compose up -d --no-deps --build frontend-react
```

---

## 📝 Useful Commands

```bash
# View all containers
docker ps -a

# View all images
docker images

# Clean up everything
docker system prune -a --volumes

# Export container
docker export metamind-backend > backend.tar

# Import container
docker import backend.tar

# View container details
docker inspect metamind-backend

# Execute command in container
docker-compose exec backend python --version

# Copy files from container
docker cp metamind-backend:/app/data/metamind.db ./local-backup.db

# Copy files to container
docker cp ./config.json metamind-backend:/app/config.json
```

---

## 🎯 Performance Optimization

### 1. Multi-stage Builds

Already implemented in React Dockerfile:
- Builder stage: ~500MB
- Production stage: ~25MB
- **Savings:** 95% size reduction

### 2. Layer Caching

Optimize Dockerfile order:
```dockerfile
# Install dependencies first (cached)
COPY package*.json ./
RUN npm ci

# Copy source code last (changes frequently)
COPY . .
```

### 3. Nginx Optimization

Already configured in `nginx.conf`:
- Gzip compression
- Static asset caching (1 year)
- Security headers

### 4. Resource Limits

Add to `docker-compose.yml`:
```yaml
services:
  backend:
    mem_limit: 2g
    cpus: 2
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## ✅ Deployment Checklist

- [ ] Environment variables configured
- [ ] Ports available (80, 8000, 8501)
- [ ] Docker and Docker Compose installed
- [ ] Sufficient disk space (10GB+)
- [ ] Sufficient RAM (4GB+)
- [ ] Firewall rules configured
- [ ] SSL certificates (production)
- [ ] Backup strategy in place
- [ ] Monitoring configured
- [ ] Health checks passing

---

*Last Updated: 2024-03-04*
*MetaMind Docker Deployment Guide* 🐳