# 📡 MetaMind API Reference

Complete reference for MetaMind's REST API endpoints.

---

## 🌐 Base URL

- **Local Development**: `http://localhost:8000`
- **Docker**: `http://localhost:8000`
- **Kubernetes**: `http://your-domain.com/api` or via port-forward

---

## 🔑 Authentication

Currently, MetaMind does not require authentication for API access. In production, consider implementing:
- API key authentication
- OAuth 2.0
- JWT tokens

---

## 📋 API Endpoints

### 1. Health Check

Check if the API is running and configured correctly.

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy",
  "llm_provider": "groq",
  "model": "llama-3.1-70b-versatile",
  "database": "./metamind.db"
}
```

**Example**:
```bash
curl http://localhost:8000/health
```

---

### 2. Design Architecture

Start a new architecture design session.

**Endpoint**: `POST /api/design`

**Request Body**:
```json
{
  "business_goal": "string",
  "domain": "healthcare|finance|ecommerce|education|legal|general",
  "modalities": ["text", "vision", "multimodal", "tabular"],
  "constraints": {
    "budget": "number (USD/month)",
    "latency_target_ms": "number (milliseconds)",
    "expected_users": "number",
    "risk_tolerance": "low|medium|high",
    "compliance_level": "low|medium|high"
  },
  "max_iterations": "number (default: 5)"
}
```

**Response**:
```json
{
  "run_id": "uuid",
  "status": "processing|completed|failed",
  "message": "string"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/design \
  -H "Content-Type: application/json" \
  -d '{
    "business_goal": "Build a customer support chatbot",
    "domain": "ecommerce",
    "modalities": ["text"],
    "constraints": {
      "budget": 5000,
      "latency_target_ms": 300,
      "expected_users": 50000,
      "risk_tolerance": "medium",
      "compliance_level": "high"
    },
    "max_iterations": 3
  }'
```

---

### 3. Get Design Status

Check the current status of a design session.

**Endpoint**: `GET /api/design/{run_id}/status`

**Path Parameters**:
- `run_id` (string, required): The design session ID

**Response**:
```json
{
  "run_id": "uuid",
  "status": "processing|completed|failed",
  "current_stage": "string",
  "progress_percentage": "number (0-100)",
  "estimated_time_remaining": "number (seconds)"
}
```

**Example**:
```bash
curl http://localhost:8000/api/design/{run_id}/status
```

---

### 4. Get Design Result

Retrieve the final design result.

**Endpoint**: `GET /api/design/{run_id}/result`

**Path Parameters**:
- `run_id` (string, required): The design session ID

**Response**:
```json
{
  "run_id": "uuid",
  "status": "completed",
  "selected_architecture": {
    "architecture_id": "uuid",
    "name": "string",
    "template": "string",
    "score": "number (0-100)",
    "modules": [
      {
        "layer": "string",
        "component": "string",
        "config": {}
      }
    ]
  },
  "metrics": {
    "cost": "number (0-100)",
    "latency": "number (0-100)",
    "risk": "number (0-100)",
    "compliance": "number (0-100)",
    "scalability": "number (0-100)",
    "complexity": "number (0-100)"
  },
  "reflection": {
    "confidence_score": "number (0.0-1.0)",
    "strengths": ["string"],
    "weaknesses": ["string"]
  }
}
```

**Example**:
```bash
curl http://localhost:8000/api/design/{run_id}/result
```

---

### 5. Get Real-time Progress

Stream real-time progress updates (Server-Sent Events).

**Endpoint**: `GET /api/design/{run_id}/progress`

**Path Parameters**:
- `run_id` (string, required): The design session ID

**Response**: Server-Sent Events stream

**Event Types**:
- `stage_update`: Current processing stage
- `candidate_generated`: New architecture candidate
- `simulation_complete`: Metrics calculated
- `iteration_complete`: Iteration finished
- `design_complete`: Final design ready

**Example**:
```bash
curl -N http://localhost:8000/api/design/{run_id}/progress
```

**JavaScript Example**:
```javascript
const eventSource = new EventSource(`/api/design/${runId}/progress`);

eventSource.addEventListener('stage_update', (event) => {
  const data = JSON.parse(event.data);
  console.log('Current stage:', data.stage);
});

eventSource.addEventListener('design_complete', (event) => {
  console.log('Design completed!');
  eventSource.close();
});
```

---

### 6. Get Version History

Retrieve all versions of an architecture design.

**Endpoint**: `GET /api/design/{run_id}/versions`

**Path Parameters**:
- `run_id` (string, required): The design session ID

**Response**:
```json
{
  "run_id": "uuid",
  "versions": [
    {
      "version": "number",
      "timestamp": "ISO-8601 datetime",
      "score": "number (0-100)",
      "changes_made": ["string"],
      "metrics": {}
    }
  ]
}
```

**Example**:
```bash
curl http://localhost:8000/api/design/{run_id}/versions
```

---

### 7. Compare Versions

Compare two versions of an architecture.

**Endpoint**: `GET /api/design/{run_id}/compare/{version1}/{version2}`

**Path Parameters**:
- `run_id` (string, required): The design session ID
- `version1` (number, required): First version number
- `version2` (number, required): Second version number

**Response**:
```json
{
  "version_1": {
    "version": "number",
    "score": "number",
    "metrics": {}
  },
  "version_2": {
    "version": "number",
    "score": "number",
    "metrics": {}
  },
  "deltas": {
    "score_delta": "number",
    "metric_deltas": {
      "cost": "number",
      "latency": "number",
      "risk": "number",
      "compliance": "number",
      "scalability": "number",
      "complexity": "number"
    }
  },
  "recommendation": "string"
}
```

**Example**:
```bash
curl http://localhost:8000/api/design/{run_id}/compare/1/2
```

---

### 8. Get Specification

Download comprehensive documentation for the design.

**Endpoint**: `GET /api/design/{run_id}/specification`

**Path Parameters**:
- `run_id` (string, required): The design session ID

**Response**:
```json
{
  "executive_summary": "markdown string",
  "technical_specification": "markdown string",
  "deployment_plan": "markdown string",
  "monitoring_strategy": "markdown string"
}
```

**Example**:
```bash
curl http://localhost:8000/api/design/{run_id}/specification
```

---

### 9. Get Design History

List all past design sessions.

**Endpoint**: `GET /api/history`

**Query Parameters**:
- `limit` (number, optional): Maximum number of results (default: 50)
- `offset` (number, optional): Pagination offset (default: 0)
- `domain` (string, optional): Filter by domain
- `status` (string, optional): Filter by status

**Response**:
```json
{
  "total": "number",
  "designs": [
    {
      "run_id": "uuid",
      "timestamp": "ISO-8601 datetime",
      "business_goal": "string",
      "domain": "string",
      "status": "string",
      "final_score": "number"
    }
  ]
}
```

**Example**:
```bash
curl "http://localhost:8000/api/history?limit=10&domain=ecommerce"
```

---

### 10. Generate Code

Generate production-ready code for the selected architecture.

**Endpoint**: `POST /api/code-generation/{run_id}/generate`

**Path Parameters**:
- `run_id` (string, required): The design session ID

**Request Body**:
```json
{
  "language": "python|javascript|typescript",
  "framework": "fastapi|express|nestjs",
  "include_docker": "boolean",
  "include_tests": "boolean",
  "include_docs": "boolean"
}
```

**Response**:
```json
{
  "project_id": "uuid",
  "status": "completed",
  "files": ["string"],
  "download_url": "string"
}
```

**Example**:
```bash
curl -X POST http://localhost:8000/api/code-generation/{run_id}/generate \
  -H "Content-Type: application/json" \
  -d '{
    "language": "python",
    "framework": "fastapi",
    "include_docker": true,
    "include_tests": true,
    "include_docs": true
  }'
```

---

### 11. Download Generated Code

Download the generated code as a ZIP file.

**Endpoint**: `GET /api/code-generation/{project_id}/download`

**Path Parameters**:
- `project_id` (string, required): The generated project ID

**Response**: ZIP file download

**Example**:
```bash
curl -O http://localhost:8000/api/code-generation/{project_id}/download
```

---

### 12. Get File Content (Code Editor)

Get the content of a specific generated file.

**Endpoint**: `GET /api/code-editor/{project_id}/file`

**Path Parameters**:
- `project_id` (string, required): The generated project ID

**Query Parameters**:
- `file_path` (string, required): Relative path to the file

**Response**:
```json
{
  "path": "string",
  "content": "string",
  "language": "string",
  "size": "number"
}
```

**Example**:
```bash
curl "http://localhost:8000/api/code-editor/{project_id}/file?file_path=app/main.py"
```

---

## 🔧 Error Responses

All endpoints return standard HTTP status codes and error responses:

### Error Response Format

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "ISO-8601 datetime"
}
```

### Common Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid request parameters |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | LLM service unavailable |

### Example Error Response

```json
{
  "detail": "Invalid domain. Must be one of: healthcare, finance, ecommerce, education, legal, general",
  "error_code": "INVALID_DOMAIN",
  "timestamp": "2026-03-09T10:30:00Z"
}
```

---

## 📊 Rate Limiting

Currently, no rate limiting is enforced. For production deployment, consider:

- **Per IP**: 100 requests per minute
- **Per API Key**: 1000 requests per hour
- **Design Endpoint**: 10 concurrent designs per user

---

## 🔍 Request/Response Examples

### Complete Design Flow

```bash
# 1. Start design
RESPONSE=$(curl -X POST http://localhost:8000/api/design \
  -H "Content-Type: application/json" \
  -d '{
    "business_goal": "Build a customer support chatbot",
    "domain": "ecommerce",
    "modalities": ["text"],
    "constraints": {
      "budget": 5000,
      "latency_target_ms": 300,
      "expected_users": 50000,
      "risk_tolerance": "medium",
      "compliance_level": "high"
    }
  }')

RUN_ID=$(echo $RESPONSE | jq -r '.run_id')
echo "Design started: $RUN_ID"

# 2. Check status
curl http://localhost:8000/api/design/$RUN_ID/status

# 3. Get result (wait for completion)
curl http://localhost:8000/api/design/$RUN_ID/result

# 4. Get versions
curl http://localhost:8000/api/design/$RUN_ID/versions

# 5. Compare versions
curl http://localhost:8000/api/design/$RUN_ID/compare/1/2

# 6. Get specification
curl http://localhost:8000/api/design/$RUN_ID/specification

# 7. Generate code
curl -X POST http://localhost:8000/api/code-generation/$RUN_ID/generate \
  -H "Content-Type: application/json" \
  -d '{"language": "python", "framework": "fastapi"}'
```

---

## 🐍 Python Client Example

```python
import requests
import time

class MetaMindClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def design_architecture(self, business_goal, domain, modalities, constraints):
        """Start a new architecture design"""
        response = requests.post(
            f"{self.base_url}/api/design",
            json={
                "business_goal": business_goal,
                "domain": domain,
                "modalities": modalities,
                "constraints": constraints
            }
        )
        response.raise_for_status()
        return response.json()["run_id"]
    
    def wait_for_completion(self, run_id, timeout=300):
        """Wait for design to complete"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            status = self.get_status(run_id)
            if status["status"] == "completed":
                return True
            elif status["status"] == "failed":
                raise Exception("Design failed")
            time.sleep(5)
        raise TimeoutError("Design timed out")
    
    def get_status(self, run_id):
        """Get design status"""
        response = requests.get(f"{self.base_url}/api/design/{run_id}/status")
        response.raise_for_status()
        return response.json()
    
    def get_result(self, run_id):
        """Get design result"""
        response = requests.get(f"{self.base_url}/api/design/{run_id}/result")
        response.raise_for_status()
        return response.json()

# Usage
client = MetaMindClient()

run_id = client.design_architecture(
    business_goal="Build a customer support chatbot",
    domain="ecommerce",
    modalities=["text"],
    constraints={
        "budget": 5000,
        "latency_target_ms": 300,
        "expected_users": 50000,
        "risk_tolerance": "medium",
        "compliance_level": "high"
    }
)

print(f"Design started: {run_id}")
client.wait_for_completion(run_id)
result = client.get_result(run_id)
print(f"Final score: {result['selected_architecture']['score']}")
```

---

## 📚 Additional Resources

- [Interactive API Documentation](http://localhost:8000/docs) - Swagger UI
- [Alternative API Documentation](http://localhost:8000/redoc) - ReDoc
- [Getting Started Guide](GETTING_STARTED.md)
- [Architecture Documentation](ARCHITECTURE.md)

---

**Complete API reference for MetaMind!** 🚀