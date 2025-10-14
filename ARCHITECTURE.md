# Architecture Documentation

## Real-Time ML Model Serving API

**Author:** Gabriel Demetrios Lafis

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Deployment Architecture](#deployment-architecture)
- [Scaling Architecture](#scaling-architecture)
- [Monitoring Architecture](#monitoring-architecture)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ Web Client │  │ Mobile App │  │  API Client │                │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘                │
└────────┼───────────────┼───────────────┼─────────────────────────┘
         │               │               │
         └───────────────┴───────────────┘
                         │
         ┌───────────────▼────────────────┐
         │      Load Balancer / Ingress   │
         └───────────────┬────────────────┘
                         │
         ┌───────────────▼────────────────┐
         │    ML Serving API (Go)         │
         │  ┌──────────────────────────┐  │
         │  │  REST API Endpoints      │  │
         │  │  - /predict              │  │
         │  │  - /health               │  │
         │  │  - /models               │  │
         │  │  - /metrics              │  │
         │  └──────────┬───────────────┘  │
         │             │                   │
         │  ┌──────────▼───────────────┐  │
         │  │  Middleware Layer        │  │
         │  │  - CORS                  │  │
         │  │  - Rate Limiting         │  │
         │  │  - Logging               │  │
         │  │  - Authentication        │  │
         │  └──────────┬───────────────┘  │
         │             │                   │
         │  ┌──────────▼───────────────┐  │
         │  │  Business Logic          │  │
         │  │  - Model Loading         │  │
         │  │  - Prediction Engine     │  │
         │  │  - Cache Management      │  │
         │  └──────────┬───────────────┘  │
         └─────────────┼───────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
   ┌─────────┐  ┌──────────┐  ┌─────────┐
   │  Redis  │  │  Models  │  │Metrics  │
   │  Cache  │  │ Storage  │  │  DB     │
   └─────────┘  └──────────┘  └─────────┘
         │             │             │
         └─────────────┴─────────────┘
                       │
         ┌─────────────▼─────────────┐
         │   Monitoring Stack        │
         │  ┌──────────────────────┐ │
         │  │    Prometheus        │ │
         │  └──────────┬───────────┘ │
         │             │              │
         │  ┌──────────▼───────────┐ │
         │  │      Grafana         │ │
         │  └──────────────────────┘ │
         └───────────────────────────┘
```

---

## Component Architecture

### Server Components (Go)

```
server/
├── main.go                    # Application entry point
│   ├── Server initialization
│   ├── Route registration
│   ├── Middleware setup
│   └── Graceful shutdown
│
├── handlers/                  # HTTP request handlers
│   ├── predict.go            # Prediction endpoint
│   ├── health.go             # Health check
│   ├── models.go             # Model management
│   └── metrics.go            # Metrics endpoint
│
├── models/                    # Model management
│   ├── loader.go             # Model loading/unloading
│   ├── predictor.go          # Prediction logic
│   ├── registry.go           # Model registry
│   └── cache.go              # Model caching
│
├── middleware/                # HTTP middleware
│   ├── cors.go               # CORS handling
│   ├── auth.go               # Authentication
│   ├── ratelimit.go          # Rate limiting
│   └── logging.go            # Request logging
│
├── cache/                     # Cache layer
│   ├── redis.go              # Redis client
│   └── strategy.go           # Caching strategies
│
└── config/                    # Configuration
    └── config.go             # Config management
```

### Client Components (Python)

```
client/
├── ml_client.py              # API client library
│   ├── MLClient class
│   ├── Prediction methods
│   └── Error handling
│
├── train_model.py            # Model training
│   ├── Data loading
│   ├── Training pipeline
│   ├── Model saving
│   └── Metadata generation
│
├── model_evaluator.py        # Model evaluation
│   ├── Performance metrics
│   ├── Drift detection
│   └── Model comparison
│
└── batch_predictor.py        # Batch predictions
    ├── Parallel processing
    ├── CSV support
    └── Streaming predictions
```

---

## Data Flow

### Prediction Request Flow

```
1. Client Request
   │
   ├─→ [HTTP POST /predict]
   │   {
   │     "model_name": "iris_classifier",
   │     "features": [5.1, 3.5, 1.4, 0.2]
   │   }
   │
2. Middleware Processing
   │
   ├─→ CORS Check ✓
   ├─→ Rate Limit Check ✓
   ├─→ Request Validation ✓
   └─→ Request Logging
   │
3. Cache Lookup
   │
   ├─→ Generate Cache Key: "pred:iris_classifier:[5.1,3.5,1.4,0.2]"
   ├─→ Query Redis
   │
   ├─→ Cache HIT? ────────────┐
   │   └─→ Return cached result│
   │                           │
   └─→ Cache MISS?            │
       │                       │
4. Model Prediction           │
   │                           │
   ├─→ Load Model             │
   ├─→ Validate Features      │
   ├─→ Run Prediction         │
   ├─→ Calculate Probability  │
   │                           │
5. Cache Storage              │
   │                           │
   ├─→ Store in Redis         │
   ├─→ Set TTL (5 minutes)    │
   │                           │
6. Response Generation ◄──────┘
   │
   ├─→ Format Response
   │   {
   │     "prediction": 0,
   │     "probability": 0.95,
   │     "latency_ms": 1.23,
   │     "cache_hit": false
   │   }
   │
7. Metrics Update
   │
   ├─→ Update request counter
   ├─→ Record latency
   ├─→ Update cache hit rate
   │
8. Return to Client
```

---

## Deployment Architecture

### Docker Compose Deployment

```
┌─────────────────────────────────────────────┐
│           Docker Host                        │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │  Docker Network: ml-network            │ │
│  │                                        │ │
│  │  ┌──────────────┐  ┌───────────────┐ │ │
│  │  │              │  │               │ │ │
│  │  │   ml-server  │  │  ml-redis     │ │ │
│  │  │   :8080      │──│  :6379        │ │ │
│  │  │   :9090      │  │               │ │ │
│  │  │              │  │               │ │ │
│  │  └──────┬───────┘  └───────────────┘ │ │
│  │         │                             │ │
│  │  ┌──────▼──────────────────────────┐ │ │
│  │  │                                  │ │ │
│  │  │   Prometheus + Grafana          │ │ │
│  │  │   :9091, :3000                  │ │ │
│  │  │                                  │ │ │
│  │  └──────────────────────────────────┘ │ │
│  │                                        │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  Volumes:                                    │
│  - redis_data                                │
│  - prometheus_data                           │
│  - grafana_data                              │
└─────────────────────────────────────────────┘
```

### Kubernetes Deployment

```
┌────────────────────────────────────────────────────────┐
│                  Kubernetes Cluster                     │
│                                                         │
│  ┌──────────────────────────────────────────────────┐ │
│  │              Ingress Controller                   │ │
│  │         (nginx-ingress / Traefik)                 │ │
│  └────────────────────┬─────────────────────────────┘ │
│                       │                                │
│  ┌────────────────────▼─────────────────────────────┐ │
│  │          Ingress: ml-server-ingress              │ │
│  │          Host: ml-api.example.com                │ │
│  └────────────────────┬─────────────────────────────┘ │
│                       │                                │
│  ┌────────────────────▼─────────────────────────────┐ │
│  │      Service: ml-server-service (LoadBalancer)   │ │
│  │           Port: 80 → 8080                        │ │
│  └────────────────────┬─────────────────────────────┘ │
│                       │                                │
│  ┌────────────────────▼─────────────────────────────┐ │
│  │      Deployment: ml-server                       │ │
│  │      Replicas: 3 (HPA: 3-10)                    │ │
│  │                                                   │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐     │ │
│  │  │  Pod 1    │ │  Pod 2    │ │  Pod 3    │     │ │
│  │  │ ml-server │ │ ml-server │ │ ml-server │     │ │
│  │  │  :8080    │ │  :8080    │ │  :8080    │     │ │
│  │  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘     │ │
│  │        │             │             │             │ │
│  └────────┼─────────────┼─────────────┼─────────────┘ │
│           │             │             │                │
│  ┌────────▼─────────────▼─────────────▼─────────────┐ │
│  │      Service: redis-service (ClusterIP)          │ │
│  │           Port: 6379                             │ │
│  └────────────────────┬─────────────────────────────┘ │
│                       │                                │
│  ┌────────────────────▼─────────────────────────────┐ │
│  │      StatefulSet: redis                          │ │
│  │      Replicas: 1                                 │ │
│  │  ┌────────────┐                                  │ │
│  │  │   redis    │                                  │ │
│  │  │   :6379    │                                  │ │
│  │  └────────────┘                                  │ │
│  └──────────────────────────────────────────────────┘ │
│                                                         │
│  Persistent Volumes:                                    │
│  - ml-models-pvc (ReadOnlyMany, 10Gi)                 │
│  - redis-pvc (ReadWriteOnce, 5Gi)                     │
│                                                         │
│  ConfigMaps:                                            │
│  - ml-server-config                                     │
│                                                         │
│  Secrets:                                               │
│  - redis-secret                                         │
└────────────────────────────────────────────────────────┘
```

---

## Scaling Architecture

### Horizontal Scaling

```
Load Balancer
     │
     ├──────────┬──────────┬──────────┬──────────┐
     │          │          │          │          │
     ▼          ▼          ▼          ▼          ▼
 Instance 1  Instance 2  Instance 3  ...    Instance N
     │          │          │          │          │
     └──────────┴──────────┴──────────┴──────────┘
                         │
                    Redis Cluster
                  ┌──────┴──────┐
                Master1      Master2
                  │              │
                Replica1      Replica2
```

### Auto-Scaling Configuration

**Kubernetes HPA:**

```yaml
minReplicas: 3
maxReplicas: 10
metrics:
  - CPU: 70%
  - Memory: 80%
  - Custom: requests_per_second > 1000
```

**Scaling Triggers:**

- CPU > 70% → Scale up
- Memory > 80% → Scale up
- Request rate > 1000/s → Scale up
- Average response time > 100ms → Scale up
- No activity for 5 minutes → Scale down

---

## Monitoring Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Application Layer                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Instance 1 │  │  Instance 2 │  │  Instance N │ │
│  │   :9090     │  │   :9090     │  │   :9090     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │         │
│         └────────────────┴────────────────┘         │
│                          │                           │
└──────────────────────────┼───────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────┐
│              Metrics Collection Layer                 │
│  ┌────────────────────────────────────────────────┐  │
│  │           Prometheus                           │  │
│  │  - Scrapes metrics every 15s                   │  │
│  │  - Stores time-series data                     │  │
│  │  - Evaluates alert rules                       │  │
│  └────────────────────┬───────────────────────────┘  │
└───────────────────────┼──────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
┌───────────────┐ ┌──────────┐ ┌──────────────┐
│   Grafana     │ │AlertManager│ │   Logs      │
│  Dashboards   │ │  Alerts   │ │ Aggregation │
│  :3000        │ │           │ │             │
└───────────────┘ └─────┬────┘ └──────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Notifications   │
              │  - Slack         │
              │  - PagerDuty     │
              │  - Email         │
              └──────────────────┘
```

### Monitored Metrics

**Application Metrics:**
- Request rate (req/s)
- Response time (p50, p95, p99)
- Error rate
- Cache hit rate
- Active connections

**System Metrics:**
- CPU usage
- Memory usage
- Disk I/O
- Network I/O

**Business Metrics:**
- Predictions per model
- Model accuracy drift
- Active models
- User sessions

---

## Security Architecture

```
┌────────────────────────────────────────────┐
│              Security Layers               │
│                                            │
│  1. Network Layer                          │
│     ├─→ TLS/SSL encryption                │
│     ├─→ Firewall rules                    │
│     └─→ DDoS protection                   │
│                                            │
│  2. Application Layer                      │
│     ├─→ API Key authentication            │
│     ├─→ Rate limiting                     │
│     ├─→ Input validation                  │
│     └─→ CORS policies                     │
│                                            │
│  3. Data Layer                             │
│     ├─→ Encrypted connections             │
│     ├─→ Access control                    │
│     └─→ Audit logging                     │
│                                            │
│  4. Infrastructure Layer                   │
│     ├─→ Network policies                  │
│     ├─→ Pod security policies             │
│     └─→ Secret management                 │
└────────────────────────────────────────────┘
```

---

## Disaster Recovery

### Backup Strategy

```
┌─────────────────────────────────────┐
│         Backup Components           │
│                                     │
│  1. Models                          │
│     ├─→ Daily snapshots             │
│     ├─→ Version control in Git      │
│     └─→ S3/Object storage           │
│                                     │
│  2. Redis Data                      │
│     ├─→ RDB snapshots (hourly)      │
│     ├─→ AOF logs (real-time)        │
│     └─→ Replica synchronization     │
│                                     │
│  3. Configuration                   │
│     ├─→ Git repository              │
│     └─→ ConfigMap backups           │
│                                     │
│  4. Metrics                         │
│     ├─→ Prometheus backups          │
│     └─→ Long-term storage           │
└─────────────────────────────────────┘
```

### Recovery Procedures

**RTO (Recovery Time Objective):** < 5 minutes  
**RPO (Recovery Point Objective):** < 15 minutes

---

## Performance Optimization

### Caching Strategy

```
┌────────────────────────────────────────┐
│          Multi-Level Caching           │
│                                        │
│  L1: In-Memory Cache (Go)              │
│      ├─→ Recent predictions            │
│      ├─→ Model metadata                │
│      └─→ TTL: 1 minute                │
│              │                          │
│  L2: Redis Cache                       │
│      ├─→ Prediction results            │
│      ├─→ Session data                  │
│      └─→ TTL: 5 minutes               │
│              │                          │
│  L3: Model Storage                     │
│      ├─→ Trained models                │
│      └─→ Persistent                    │
└────────────────────────────────────────┘
```

---

## Conclusion

This architecture provides:

✅ High availability with redundancy  
✅ Horizontal scalability  
✅ Sub-millisecond latency  
✅ Comprehensive monitoring  
✅ Security best practices  
✅ Disaster recovery capabilities  

For questions or improvements, please open an issue on GitHub.
