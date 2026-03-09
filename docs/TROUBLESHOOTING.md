# 🔧 MetaMind Troubleshooting Guide

Common issues and their solutions.

---

## 🚨 Common Issues

### Backend Issues

#### Issue: "Connection refused" to backend

**Symptoms**:
- Frontend can't connect to API
- `curl http://localhost:8000/health` fails

**Solutions**:

1. **Check if backend is running**:
```bash
# Docker
docker-compose ps
docker-compose logs backend

# Local
ps aux | grep python
```

2. **Start backend**:
```bash
# Docker
docker-compose up -d backend

# Local
cd backend
source venv/bin/activate
python run_backend.py
```

3. **Check port conflicts**:
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill process if needed
kill -9 <PID>
```

---

#### Issue: "Invalid API key" or "LLM service unavailable"

**Symptoms**:
- Design requests fail
- Error: "Invalid API key"
- Error: "Failed to connect to LLM service"

**Solutions**:

1. **Verify API key**:
```bash
# Check .env file
cat .env | grep GROQ_API_KEY

# Test API key
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

2. **Get new API key**:
- Visit [console.groq.com](https://console.groq.com/)
- Create new API key
- Update `.env` file
- Restart backend

3. **Check API key format**:
```env
# Correct format
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx

# Wrong format (no quotes needed)
GROQ_API_KEY="gsk_xxxxxxxxxxxxxxxxxxxxx"
```

---

#### Issue: "Database locked" error

**Symptoms**:
- Error: "database is locked"
- Can't save designs
- Slow database operations

**Solutions**:

1. **Stop all backend instances**:
```bash
# Docker
docker-compose stop backend

# Local
pkill -f "python run_backend.py"
```

2. **Remove lock file**:
```bash
rm metamind.db-journal
```

3. **Restart backend**:
```bash
docker-compose up -d backend
```

4. **If problem persists, reset database**:
```bash
# Backup first
cp metamind.db metamind.db.backup

# Remove database
rm metamind.db

# Restart backend (will create new database)
docker-compose restart backend
```

---

#### Issue: Slow performance / Timeouts

**Symptoms**:
- Design takes > 10 minutes
- Requests timeout
- High CPU usage

**Solutions**:

1. **Use smaller model**:
```env
# In .env file
GROQ_MODEL=llama-3.1-8b-instant  # Instead of 70b
```

2. **Reduce iterations**:
```json
{
  "max_iterations": 2  // Instead of 5
}
```

3. **Check system resources**:
```bash
# Check CPU and memory
top
htop

# Check Docker resources
docker stats
```

4. **Increase timeout**:
```python
# In backend/utils/llm_utils.py
timeout = 300  # Increase from default
```

---

### Frontend Issues

#### Issue: Frontend not loading / Blank page

**Symptoms**:
- White screen
- "Cannot GET /" error
- Console errors

**Solutions**:

1. **Check if frontend is running**:
```bash
# Docker
docker-compose ps frontend-react
docker-compose logs frontend-react

# Local
ps aux | grep vite
```

2. **Start frontend**:
```bash
# Docker
docker-compose up -d frontend-react

# Local
cd frontend-react
npm run dev
```

3. **Clear browser cache**:
- Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
- Clear cache in browser settings
- Try incognito/private mode

4. **Check console for errors**:
- Open DevTools (F12)
- Check Console tab
- Look for error messages

---

#### Issue: "Failed to fetch" or CORS errors

**Symptoms**:
- API calls fail
- Console error: "CORS policy"
- Network errors in DevTools

**Solutions**:

1. **Check backend CORS configuration**:
```python
# In backend/api/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Update .env file**:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

3. **Restart backend**:
```bash
docker-compose restart backend
```

---

#### Issue: Monaco Editor not loading files

**Symptoms**:
- Code editor shows template content
- Files don't load
- "Error loading file" message

**Solutions**:

1. **Check backend API**:
```bash
# Test file endpoint
curl "http://localhost:8000/api/code-editor/{project_id}/file?file_path=main.py"
```

2. **Check browser console**:
- Look for 404 or 500 errors
- Check Network tab in DevTools

3. **Verify project ID**:
- Ensure project was generated successfully
- Check that files exist in generated_projects directory

---

### Docker Issues

#### Issue: "Cannot connect to Docker daemon"

**Symptoms**:
- `docker-compose up` fails
- Error: "Cannot connect to the Docker daemon"

**Solutions**:

1. **Start Docker**:
```bash
# macOS
open -a Docker

# Linux
sudo systemctl start docker

# Windows
# Start Docker Desktop
```

2. **Check Docker status**:
```bash
docker info
docker ps
```

---

#### Issue: "Port already in use"

**Symptoms**:
- Error: "port is already allocated"
- Can't start containers

**Solutions**:

1. **Find process using port**:
```bash
# Port 8000 (backend)
lsof -i :8000

# Port 5173 (frontend)
lsof -i :5173
```

2. **Kill process**:
```bash
kill -9 <PID>
```

3. **Or change port in docker-compose.yml**:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Use different external port
```

---

#### Issue: "No space left on device"

**Symptoms**:
- Can't build images
- Can't start containers
- Disk space errors

**Solutions**:

1. **Clean up Docker**:
```bash
# Remove unused containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a --volumes
```

2. **Check disk space**:
```bash
df -h
docker system df
```

---

### Kubernetes Issues

#### Issue: Pods not starting

**Symptoms**:
- `kubectl get pods` shows CrashLoopBackOff
- Pods in Pending state
- ImagePullBackOff errors

**Solutions**:

1. **Check pod logs**:
```bash
kubectl logs -n metamind <pod-name>
kubectl describe pod -n metamind <pod-name>
```

2. **Check events**:
```bash
kubectl get events -n metamind --sort-by='.lastTimestamp'
```

3. **Common fixes**:

**ImagePullBackOff**:
```bash
# Build and push images
docker build -t metamind-backend:latest -f Dockerfile.backend .
docker build -t metamind-frontend-react:latest -f Dockerfile.frontend .

# For Minikube, use local images
eval $(minikube docker-env)
docker build -t metamind-backend:latest -f Dockerfile.backend .
```

**CrashLoopBackOff**:
```bash
# Check logs for errors
kubectl logs -n metamind <pod-name> --previous

# Common causes:
# - Missing API key in secret
# - Database connection issues
# - Port conflicts
```

---

#### Issue: Can't access application

**Symptoms**:
- Port-forward doesn't work
- Ingress not accessible
- Connection refused

**Solutions**:

1. **Check services**:
```bash
kubectl get svc -n metamind
kubectl describe svc -n metamind metamind-frontend-react
```

2. **Test port-forward**:
```bash
# Forward to backend
kubectl port-forward -n metamind svc/metamind-backend 8000:8000

# Test
curl http://localhost:8000/health
```

3. **Check ingress**:
```bash
kubectl get ingress -n metamind
kubectl describe ingress -n metamind
```

---

### API Issues

#### Issue: Design request hangs / Never completes

**Symptoms**:
- Request takes > 10 minutes
- No progress updates
- Status stuck at "processing"

**Solutions**:

1. **Check backend logs**:
```bash
# Docker
docker-compose logs -f backend

# Kubernetes
kubectl logs -n metamind -l component=backend -f
```

2. **Check for errors**:
- LLM API errors
- Timeout errors
- Memory issues

3. **Restart backend**:
```bash
# Docker
docker-compose restart backend

# Kubernetes
kubectl rollout restart deployment/metamind-backend -n metamind
```

---

#### Issue: "422 Unprocessable Entity" errors

**Symptoms**:
- API returns 422 status
- Validation errors
- "Field required" errors

**Solutions**:

1. **Check request format**:
```json
{
  "business_goal": "string",  // Required
  "domain": "ecommerce",      // Must be valid domain
  "modalities": ["text"],     // Must be array
  "constraints": {            // All fields required
    "budget": 5000,
    "latency_target_ms": 300,
    "expected_users": 50000,
    "risk_tolerance": "medium",
    "compliance_level": "high"
  }
}
```

2. **Valid values**:
- **domain**: healthcare, finance, ecommerce, education, legal, general
- **modalities**: text, vision, multimodal, tabular
- **risk_tolerance**: low, medium, high
- **compliance_level**: low, medium, high

---

## 🔍 Debugging Tips

### Enable Debug Logging

**Backend**:
```env
# In .env file
LOG_LEVEL=DEBUG
```

**Frontend**:
```typescript
// In src/services/api.ts
const DEBUG = true;

if (DEBUG) {
  console.log('API Request:', url, options);
  console.log('API Response:', response);
}
```

### Check Health Endpoints

```bash
# Backend health
curl http://localhost:8000/health

# Expected response
{
  "status": "healthy",
  "llm_provider": "groq",
  "model": "llama-3.1-70b-versatile",
  "database": "./metamind.db"
}
```

### Monitor Resource Usage

```bash
# Docker
docker stats

# Kubernetes
kubectl top pods -n metamind
kubectl top nodes
```

### View Database

```bash
# SQLite
sqlite3 metamind.db
.tables
SELECT * FROM runs;
SELECT * FROM architectures;
.quit
```

---

## 📞 Getting Help

If you can't resolve the issue:

1. **Check logs**:
```bash
# Docker
docker-compose logs -f

# Kubernetes
kubectl logs -n metamind -l app=metamind --tail=100
```

2. **Search existing issues**:
- [GitHub Issues](https://github.com/yourusername/metamind/issues)

3. **Create new issue**:
- Include error messages
- Include logs
- Include steps to reproduce
- Include environment details (OS, Docker version, etc.)

4. **Ask in discussions**:
- [GitHub Discussions](https://github.com/yourusername/metamind/discussions)

---

## 📚 Additional Resources

- [Getting Started Guide](GETTING_STARTED.md)
- [Deployment Guide](DEPLOYMENT.md)
- [API Reference](API_REFERENCE.md)
- [Development Guide](DEVELOPMENT.md)

---

**Still having issues? Open an issue on GitHub!** 🆘