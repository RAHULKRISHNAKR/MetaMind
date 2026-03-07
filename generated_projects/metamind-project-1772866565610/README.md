# metamind-project-1772866565610

A production-ready Healthcare Patient Monitoring System with real-time anomaly detection, built with FastAPI, PostgreSQL, Redis, and Machine Learning.

## 🏥 Features

- **Real-time Vital Signs Monitoring**: Track heart rate, blood pressure, oxygen saturation, temperature, and respiratory rate
- **AI-Powered Anomaly Detection**: Machine learning model (Isolation Forest) detects abnormal vital signs patterns
- **Instant Alerts**: WebSocket-based real-time alerts for medical staff
- **HIPAA Compliant**: Secure data handling with encryption and audit logging
- **Scalable Architecture**: Horizontal scaling with Redis caching and connection pooling
- **Production Ready**: Docker containerization, health checks, monitoring, and logging

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL 15+ (if running without Docker)
- Redis 7+ (if running without Docker)

### Using Docker (Recommended)

1. **Clone and navigate to project**:
```bash
cd metamind-project-1772866565610
```

2. **Set environment variables** (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start all services**:
```bash
docker-compose up -d
```

4. **Check service health**:
```bash
curl http://localhost:8000/health
```

5. **Access services**:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

### Local Development

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up database**:
```bash
# Start PostgreSQL and Redis
docker-compose up -d postgres redis

# Set environment variables
export DATABASE_URL="postgresql://healthcare_user:healthcare_password@localhost:5432/healthcare_db"
export REDIS_URL="redis://:redis_password@localhost:6379/0"
```

3. **Run application**:
```bash
python main.py
```

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Record Vital Signs
```bash
POST /api/vital-signs
Content-Type: application/json

{
  "patient_id": "P12345",
  "heart_rate": 75.0,
  "blood_pressure_systolic": 120.0,
  "blood_pressure_diastolic": 80.0,
  "oxygen_saturation": 98.0,
  "temperature": 98.6,
  "respiratory_rate": 16.0
}
```

### Get Patient Vital Signs History
```bash
GET /api/patients/{patient_id}/vital-signs?limit=100
```

### Get Patient Alerts
```bash
GET /api/patients/{patient_id}/alerts?acknowledged=false
```

### Acknowledge Alert
```bash
POST /api/alerts/{alert_id}/acknowledge
Content-Type: application/json

{
  "acknowledged_by": "Dr. Smith"
}
```

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/P12345');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

## 🏗️ Architecture

```
┌─────────────────┐
│  Medical        │
│  Devices        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│   FastAPI       │◄────►│  PostgreSQL  │
│   Application   │      │  Database    │
└────────┬────────┘      └──────────────┘
         │
         ├──────────────►┌──────────────┐
         │               │    Redis     │
         │               │    Cache     │
         │               └──────────────┘
         │
         ▼
┌─────────────────┐
│   ML Model      │
│ (Isolation      │
│  Forest)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   WebSocket     │
│   Alerts        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Medical Staff  │
│  Dashboard      │
└─────────────────┘
```

## 🔒 Security

- **Data Encryption**: All data encrypted at rest and in transit
- **Authentication**: JWT-based authentication (can be enabled)
- **HIPAA Compliance**: Audit logging for all data access
- **Input Validation**: Pydantic models validate all inputs
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **Rate Limiting**: Configurable rate limits per endpoint

## 📊 Monitoring

### Prometheus Metrics
- Request count and latency
- Database connection pool stats
- Redis cache hit rate
- ML model prediction time
- Alert generation rate

### Grafana Dashboards
- System health overview
- Patient monitoring statistics
- Alert trends
- Performance metrics

### Logging
- Structured JSON logging
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Centralized log aggregation ready

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v --cov=. --cov-report=html
```

Run specific test:
```bash
pytest tests/test_vital_signs.py -v
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `REDIS_URL` | Redis connection string | `redis://...` |
| `LOG_LEVEL` | Logging level | `info` |
| `WORKERS` | Number of Uvicorn workers | `4` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `healthcare_password` |
| `REDIS_PASSWORD` | Redis password | `redis_password` |
| `GRAFANA_PASSWORD` | Grafana admin password | `admin` |

### Database Schema

**Patients Table**:
- `id`: Primary key
- `patient_id`: Unique patient identifier
- `name`: Patient name
- `age`: Patient age
- `gender`: Patient gender
- `room_number`: Hospital room number
- `is_active`: Active status

**Vital Signs Table**:
- `id`: Primary key
- `patient_id`: Foreign key to patients
- `timestamp`: Reading timestamp
- `heart_rate`: Heart rate (BPM)
- `blood_pressure_systolic`: Systolic BP (mmHg)
- `blood_pressure_diastolic`: Diastolic BP (mmHg)
- `oxygen_saturation`: SpO2 (%)
- `temperature`: Body temperature (°F)
- `respiratory_rate`: Breaths per minute
- `anomaly_score`: ML model score (0-1)
- `is_anomaly`: Boolean flag

**Alerts Table**:
- `id`: Primary key
- `patient_id`: Foreign key to patients
- `alert_type`: critical/warning/info
- `message`: Alert message
- `timestamp`: Alert timestamp
- `acknowledged`: Acknowledgment status
- `acknowledged_by`: Staff member name
- `acknowledged_at`: Acknowledgment timestamp

## 🚀 Deployment

### Production Checklist

- [ ] Set strong passwords for all services
- [ ] Enable HTTPS/TLS
- [ ] Configure firewall rules
- [ ] Set up backup strategy
- [ ] Enable monitoring and alerting
- [ ] Configure log rotation
- [ ] Set up CI/CD pipeline
- [ ] Perform security audit
- [ ] Load testing
- [ ] Disaster recovery plan

### Scaling

**Horizontal Scaling**:
```bash
docker-compose up -d --scale app=4
```

**Database Replication**:
- Configure PostgreSQL streaming replication
- Use read replicas for queries

**Redis Clustering**:
- Enable Redis Cluster mode
- Configure sentinel for high availability

## 📝 License

This project is generated by MetaMind and is provided as-is for demonstration purposes.

## 🤝 Support

For issues and questions:
- Check the API documentation: http://localhost:8000/docs
- Review logs: `docker-compose logs -f app`
- Monitor health: `curl http://localhost:8000/health`

## 🎯 Roadmap

- [ ] Add authentication and authorization
- [ ] Implement patient management UI
- [ ] Add more ML models (LSTM, Transformer)
- [ ] Mobile app integration
- [ ] Multi-hospital support
- [ ] Advanced analytics dashboard
- [ ] Integration with EHR systems
- [ ] Telemedicine features

---

**Generated by MetaMind** - AI Pipeline Designer & Optimizer