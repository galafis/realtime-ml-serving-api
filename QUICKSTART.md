# 🚀 Quick Start Guide

Get up and running with the Real-Time ML Model Serving API in 5 minutes!

---

## Prerequisites

- Docker & Docker Compose
- OR Go 1.21+ and Python 3.8+

---

## Option 1: Docker (Recommended) 🐳

### 1. Clone the Repository

```bash
git clone https://github.com/galafis/realtime-ml-serving-api.git
cd realtime-ml-serving-api
```

### 2. Start Services

```bash
cd docker
docker-compose up -d
```

This starts:
- ML Server on http://localhost:8080
- Redis cache
- Prometheus (optional, with monitoring profile)
- Grafana (optional, with monitoring profile)

### 3. Verify Services

```bash
# Check if services are running
docker-compose ps

# Check API health
curl http://localhost:8080/health
```

### 4. Make Your First Prediction

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "iris_classifier",
    "features": [5.1, 3.5, 1.4, 0.2]
  }'
```

Expected response:
```json
{
  "prediction": 0,
  "probability": 0.85,
  "model_name": "iris_classifier",
  "latency_ms": 1.23,
  "cache_hit": false
}
```

### 5. Stop Services

```bash
docker-compose down
```

---

## Option 2: Manual Setup 🔧

### 1. Clone and Install

```bash
# Clone repository
git clone https://github.com/galafis/realtime-ml-serving-api.git
cd realtime-ml-serving-api

# Install dependencies
make install
```

### 2. Start Redis

```bash
# Using Docker
docker run -d -p 6379:6379 redis:latest

# OR using Makefile
make redis-start
```

### 3. Train Models (First Time Only)

```bash
make train-models
```

### 4. Build and Run Server

```bash
# Build
make build

# Run
make run
```

Server starts on http://localhost:8080

### 5. Test the API

In a new terminal:

```bash
# Health check
curl http://localhost:8080/health

# List models
curl http://localhost:8080/models

# Make prediction
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"model_name":"iris_classifier","features":[5.1,3.5,1.4,0.2]}'
```

---

## Using the Python Client 🐍

### 1. Install Client

```bash
pip install -r requirements.txt
```

### 2. Use the Client

Create a file `test_client.py`:

```python
from client.ml_client import MLClient

# Initialize client
client = MLClient(base_url="http://localhost:8080")

# Check health
if client.health_check():
    print("✓ API is healthy")

# List models
models = client.list_models()
print(f"Available models: {models['count']}")

# Make prediction
result = client.predict(
    model_name="iris_classifier",
    features=[5.1, 3.5, 1.4, 0.2]
)
print(f"Prediction: {result['prediction']}")
print(f"Latency: {result['latency_ms']:.2f}ms")
print(f"Cached: {result['cache_hit']}")

# Benchmark
stats = client.benchmark(
    model_name="iris_classifier",
    features=[5.1, 3.5, 1.4, 0.2],
    n_requests=100
)
print(f"Mean latency: {stats['mean_latency_ms']:.2f}ms")
print(f"P99 latency: {stats['p99_latency_ms']:.2f}ms")
```

Run it:

```bash
python test_client.py
```

---

## Batch Predictions 📊

```python
from client.batch_predictor import BatchPredictor

predictor = BatchPredictor(base_url="http://localhost:8080")

# Batch prediction
features_list = [
    [5.1, 3.5, 1.4, 0.2],
    [6.2, 2.9, 4.3, 1.3],
    [7.3, 2.9, 6.3, 1.8]
]

results = predictor.predict_batch(
    model_name="iris_classifier",
    features_list=features_list,
    parallel=True
)

for i, result in enumerate(results):
    print(f"Sample {i+1}: Prediction = {result['prediction']}")
```

---

## View Metrics 📈

Access metrics at:

```bash
# API metrics
curl http://localhost:8080/metrics

# Prometheus metrics (if monitoring enabled)
# Open in browser: http://localhost:9091

# Grafana dashboards (if monitoring enabled)
# Open in browser: http://localhost:3000
# Default credentials: admin / admin
```

---

## Common Commands

```bash
# Using Makefile
make help           # Show all commands
make install        # Install dependencies
make build          # Build server
make test           # Run tests
make lint           # Lint code
make docker-up      # Start Docker services
make docker-down    # Stop Docker services
make train-models   # Train ML models
make clean          # Clean build artifacts

# Using Docker Compose
docker-compose up -d              # Start services
docker-compose ps                 # Check status
docker-compose logs -f server     # View logs
docker-compose down               # Stop services
docker-compose restart server     # Restart server
```

---

## Testing

### Run Tests

```bash
# All tests
make test

# Go tests only
make test-go

# Python tests only
make test-python

# Integration tests
make test-integration

# Load tests
make test-load
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8080
lsof -i :8080

# Kill the process
kill -9 <PID>
```

### Redis Connection Failed

```bash
# Check if Redis is running
docker ps | grep redis

# Restart Redis
docker restart ml-redis
# OR
make redis-stop && make redis-start
```

### Models Not Found

```bash
# Train models
make train-models

# Check models directory
ls -la models/
```

### Import Errors (Python)

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or using virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Next Steps

Now that you have the API running:

1. 📖 Read the [API Documentation](API.md)
2. 🏗️ Review [Architecture](ARCHITECTURE.md)
3. 🤝 Check [Contributing Guidelines](CONTRIBUTING.md)
4. 🚀 Deploy to production using [Kubernetes manifests](kubernetes/)
5. 📊 Set up monitoring with Prometheus & Grafana

---

## Quick Reference

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/predict` | POST | Single prediction |
| `/models` | GET | List models |
| `/metrics` | GET | API metrics |

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_ADDR` | `localhost:6379` | Redis address |
| `REDIS_PASSWORD` | `` | Redis password |
| `SERVER_PORT` | `8080` | Server port |
| `LOG_LEVEL` | `info` | Log level |

### Model Files

| File | Size | Description |
|------|------|-------------|
| `iris_classifier.pkl` | 183KB | Iris species classifier |
| `binary_classifier.pkl` | 140KB | Binary classifier |

---

## Support

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/galafis/realtime-ml-serving-api/issues)
- 💬 [Discussions](https://github.com/galafis/realtime-ml-serving-api/discussions)

---

**Happy Coding!** 🚀

For detailed documentation, see [README.md](README.md)
