# API Documentation

## Real-Time ML Model Serving API

**Version:** 1.0.0  
**Base URL:** `http://localhost:8080`  
**Author:** Gabriel Demetrios Lafis

---

## Table of Contents

- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Predict](#predict)
  - [Batch Predict](#batch-predict)
  - [List Models](#list-models)
  - [Get Model Info](#get-model-info)
  - [Get Metrics](#get-metrics)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

---

## Authentication

Currently, the API does not require authentication. For production use, implement API key authentication or OAuth2.

**Future:** Set `AUTH_ENABLED=true` and configure API keys in environment variables.

---

## Endpoints

### Health Check

Check if the API is running and healthy.

**Endpoint:** `GET /health`

**Response:**

```json
{
  "status": "healthy",
  "timestamp": 1699564800,
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is unhealthy

**cURL Example:**

```bash
curl http://localhost:8080/health
```

---

### Predict

Make a single prediction using a trained model.

**Endpoint:** `POST /predict`

**Request Body:**

```json
{
  "model_name": "iris_classifier",
  "features": [5.1, 3.5, 1.4, 0.2],
  "model_version": "1.0.0"  // Optional
}
```

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `model_name` | string | Yes | Name of the model to use |
| `features` | array[float] | Yes | Feature values for prediction |
| `model_version` | string | No | Specific model version |

**Response:**

```json
{
  "prediction": 0,
  "probability": 0.95,
  "model_name": "iris_classifier",
  "model_version": "1.0.0",
  "latency_ms": 1.23,
  "cache_hit": false
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | int/float | Predicted value |
| `probability` | float | Prediction confidence (0-1) |
| `model_name` | string | Model used |
| `model_version` | string | Model version |
| `latency_ms` | float | Request latency in milliseconds |
| `cache_hit` | boolean | Whether result was cached |

**Status Codes:**
- `200 OK` - Prediction successful
- `400 Bad Request` - Invalid input
- `404 Not Found` - Model not found
- `500 Internal Server Error` - Prediction failed

**cURL Example:**

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "iris_classifier",
    "features": [5.1, 3.5, 1.4, 0.2]
  }'
```

**Python Example:**

```python
import requests

response = requests.post(
    "http://localhost:8080/predict",
    json={
        "model_name": "iris_classifier",
        "features": [5.1, 3.5, 1.4, 0.2]
    }
)
result = response.json()
print(f"Prediction: {result['prediction']}")
```

---

### Batch Predict

Make multiple predictions in a single request.

**Endpoint:** `POST /api/v1/batch_predict`

**Request Body:**

```json
{
  "model_name": "iris_classifier",
  "features_batch": [
    [5.1, 3.5, 1.4, 0.2],
    [6.2, 2.9, 4.3, 1.3],
    [7.3, 2.9, 6.3, 1.8]
  ]
}
```

**Response:**

```json
{
  "predictions": [0, 1, 2],
  "probabilities": [0.95, 0.89, 0.92],
  "total_latency_ms": 5.67,
  "count": 3
}
```

**Status Codes:**
- `200 OK` - Predictions successful
- `400 Bad Request` - Invalid input
- `413 Payload Too Large` - Batch size exceeds limit

---

### List Models

Get list of available models.

**Endpoint:** `GET /models`

**Response:**

```json
{
  "models": [
    {
      "name": "iris_classifier",
      "version": "1.0.0",
      "status": "active",
      "description": "Iris species classifier",
      "loaded_at": "2024-01-15T10:30:00Z"
    },
    {
      "name": "fraud_detector",
      "version": "2.1.0",
      "status": "active",
      "description": "Transaction fraud detector",
      "loaded_at": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 2
}
```

**Status Codes:**
- `200 OK` - Success

**cURL Example:**

```bash
curl http://localhost:8080/models
```

---

### Get Model Info

Get detailed information about a specific model.

**Endpoint:** `GET /api/v1/models/{model_name}`

**Response:**

```json
{
  "name": "iris_classifier",
  "version": "1.0.0",
  "status": "active",
  "description": "Iris species classifier using Random Forest",
  "features": ["sepal_length", "sepal_width", "petal_length", "petal_width"],
  "metrics": {
    "accuracy": 0.9667,
    "f1_score": 0.9654
  },
  "loaded_at": "2024-01-15T10:30:00Z",
  "predictions_count": 15234,
  "cache_hit_rate": 0.87
}
```

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Model not found

---

### Get Metrics

Get API performance metrics.

**Endpoint:** `GET /metrics`

**Response:**

```json
{
  "total_requests": 15234,
  "cache_hit_rate": 0.87,
  "avg_latency_ms": 0.8,
  "p50_latency_ms": 0.6,
  "p95_latency_ms": 2.3,
  "p99_latency_ms": 4.2,
  "error_rate": 0.001,
  "uptime_seconds": 86400,
  "models_loaded": 2
}
```

**Status Codes:**
- `200 OK` - Success

**cURL Example:**

```bash
curl http://localhost:8080/metrics
```

---

## Error Handling

All errors follow a consistent format:

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": "Additional error details",
  "timestamp": 1699564800
}
```

**Common Error Codes:**

| Code | Description |
|------|-------------|
| `INVALID_INPUT` | Request validation failed |
| `MODEL_NOT_FOUND` | Requested model doesn't exist |
| `PREDICTION_FAILED` | Model prediction error |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `INTERNAL_ERROR` | Server error |

**Example Error Response:**

```json
{
  "error": "Model not found",
  "code": "MODEL_NOT_FOUND",
  "details": "Model 'nonexistent_model' is not loaded",
  "timestamp": 1699564800
}
```

---

## Rate Limiting

**Default Limits:**
- 1000 requests per second per IP
- Burst: 2000 requests

**Headers:**

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1699564800
```

**Rate Limit Exceeded:**

```json
{
  "error": "Rate limit exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 60
}
```

---

## Examples

### Complete Python Client

```python
import requests
from typing import List, Dict

class MLClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def predict(self, model_name: str, features: List[float]) -> Dict:
        """Make a prediction."""
        response = self.session.post(
            f"{self.base_url}/predict",
            json={"model_name": model_name, "features": features}
        )
        response.raise_for_status()
        return response.json()
    
    def list_models(self) -> Dict:
        """List available models."""
        response = self.session.get(f"{self.base_url}/models")
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> bool:
        """Check if API is healthy."""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False

# Usage
client = MLClient()
if client.health_check():
    result = client.predict("iris_classifier", [5.1, 3.5, 1.4, 0.2])
    print(f"Prediction: {result['prediction']}")
```

### Complete Go Client

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
)

type PredictRequest struct {
    ModelName string    `json:"model_name"`
    Features  []float64 `json:"features"`
}

type PredictResponse struct {
    Prediction  int     `json:"prediction"`
    Probability float64 `json:"probability"`
    LatencyMs   float64 `json:"latency_ms"`
}

func predict(modelName string, features []float64) (*PredictResponse, error) {
    reqBody := PredictRequest{
        ModelName: modelName,
        Features:  features,
    }
    
    jsonData, _ := json.Marshal(reqBody)
    resp, err := http.Post(
        "http://localhost:8080/predict",
        "application/json",
        bytes.NewBuffer(jsonData),
    )
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var result PredictResponse
    json.NewDecoder(resp.Body).Decode(&result)
    return &result, nil
}

func main() {
    result, _ := predict("iris_classifier", []float64{5.1, 3.5, 1.4, 0.2})
    fmt.Printf("Prediction: %d\n", result.Prediction)
}
```

### cURL Examples

**Make Prediction:**

```bash
curl -X POST http://localhost:8080/predict \
  -H "Content-Type: application/json" \
  -d '{"model_name":"iris_classifier","features":[5.1,3.5,1.4,0.2]}'
```

**List Models:**

```bash
curl http://localhost:8080/models
```

**Health Check:**

```bash
curl http://localhost:8080/health
```

**Get Metrics:**

```bash
curl http://localhost:8080/metrics
```

---

## Prometheus Metrics

**Endpoint:** `http://localhost:9090/metrics`

Available metrics:
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request duration histogram
- `cache_hits_total` - Cache hits
- `cache_misses_total` - Cache misses
- `model_predictions_total` - Total predictions per model
- `model_errors_total` - Prediction errors per model

---

## WebSocket Support (Future)

Real-time predictions via WebSocket:

```javascript
const ws = new WebSocket('ws://localhost:8080/ws/predict');

ws.onopen = () => {
    ws.send(JSON.stringify({
        model_name: 'iris_classifier',
        features: [5.1, 3.5, 1.4, 0.2]
    }));
};

ws.onmessage = (event) => {
    const result = JSON.parse(event.data);
    console.log('Prediction:', result.prediction);
};
```

---

## Support

- 📧 Issues: [GitHub Issues](https://github.com/galafis/realtime-ml-serving-api/issues)
- 📖 Documentation: [README](../README.md)
- 💬 Discussions: [GitHub Discussions](https://github.com/galafis/realtime-ml-serving-api/discussions)
