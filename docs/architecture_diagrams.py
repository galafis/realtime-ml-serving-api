#!/usr/bin/env python3
"""
Generate architecture diagram for README
Author: Gabriel Demetrios Lafis
"""

# Simple ASCII art diagrams that can be embedded in README

SYSTEM_ARCHITECTURE = """
┌─────────────────────────────────────────────────────────────────┐
│                        Client Applications                       │
│          (Python, JavaScript, Go, cURL, Postman)                │
└────────────────┬────────────────────────────────────────────────┘
                 │ HTTP/REST API
                 │
┌────────────────▼────────────────────────────────────────────────┐
│                    Load Balancer / Ingress                       │
│                  (Nginx, Traefik, AWS ALB)                       │
└────────────────┬────────────────────────────────────────────────┘
                 │
         ┌───────┴───────┐
         │               │
┌────────▼──────┐ ┌─────▼─────────┐
│  ML Server    │ │  ML Server    │  ... (Auto-scaled instances)
│  Instance 1   │ │  Instance 2   │
│  (Go/Gin)     │ │  (Go/Gin)     │
└───────┬───────┘ └───────┬───────┘
        │                 │
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │  Redis Cache    │
        │  (Predictions)  │
        └─────────────────┘

External Services:
┌──────────────┐  ┌───────────────┐  ┌──────────────┐
│  Prometheus  │  │    Grafana    │  │    MLflow    │
│  (Metrics)   │  │  (Dashboard)  │  │   (Models)   │
└──────────────┘  └───────────────┘  └──────────────┘
"""

REQUEST_FLOW = """
Request Flow:
=============

1. Client Request
   │
   ├─► POST /predict
   │   {
   │     "model_name": "iris_classifier",
   │     "features": [5.1, 3.5, 1.4, 0.2]
   │   }
   │
2. Load Balancer
   │
   ├─► Routes to available ML Server instance
   │
3. ML Server Processing
   │
   ├─► Check Redis Cache
   │   │
   │   ├─► Cache HIT: Return cached prediction (< 1ms)
   │   │
   │   └─► Cache MISS: 
   │       │
   │       ├─► Load Model
   │       ├─► Make Prediction
   │       ├─► Store in Cache (TTL: 5 min)
   │       └─► Return Response
   │
4. Response to Client
   {
     "prediction": 0,
     "probability": 0.95,
     "model_name": "iris_classifier",
     "model_version": "1.0.0",
     "latency_ms": 0.8,
     "cache_hit": true
   }
"""

DATA_FLOW = """
Data Flow Architecture:
======================

Training Phase:
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Raw Data   │────▶│   Training   │────▶│   Trained   │
│  (CSV/DB)   │     │   Pipeline   │     │    Model    │
└─────────────┘     │  (Python/    │     │   (.pkl)    │
                    │   Sklearn)   │     └──────┬──────┘
                    └──────────────┘            │
                                                │
                                      ┌─────────▼────────┐
                                      │  Model Registry  │
                                      │    (MLflow)      │
                                      └─────────┬────────┘
                                                │
Serving Phase:                                  │
                                                │
┌─────────────┐                    ┌────────────▼───────┐
│   Client    │                    │    ML Server       │
│  Request    │────────────────────▶    (Go/Gin)        │
└─────────────┘  POST /predict     │  ┌──────────────┐  │
                                   │  │ Model Loader │  │
                                   │  └──────────────┘  │
                                   │  ┌──────────────┐  │
                                   │  │  Predictor   │  │
                                   │  └──────────────┘  │
                                   │  ┌──────────────┐  │
                                   │  │ Redis Cache  │  │
                                   │  └──────────────┘  │
                                   └────────────────────┘
"""

DEPLOYMENT_ARCHITECTURE = """
Kubernetes Deployment:
=====================

┌─────────────────────────────────────────────────────────┐
│                    Kubernetes Cluster                    │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │                 Ingress Controller                  │ │
│  │              ml-api.example.com (TLS)               │ │
│  └──────────────────────┬─────────────────────────────┘ │
│                         │                                │
│  ┌──────────────────────▼─────────────────────────────┐ │
│  │         Service: ml-server-service                  │ │
│  │              (LoadBalancer, Port: 80)               │ │
│  └──────────────────────┬─────────────────────────────┘ │
│                         │                                │
│           ┌─────────────┼─────────────┐                 │
│           │             │             │                  │
│  ┌────────▼──────┐ ┌───▼───────┐ ┌──▼────────┐        │
│  │   Pod 1       │ │  Pod 2    │ │  Pod 3    │ ...    │
│  │ ┌───────────┐ │ │┌─────────┐│ │┌─────────┐│        │
│  │ │ ml-server │ │ ││ml-server││ ││ml-server││        │
│  │ │  :8080    │ │ ││  :8080  ││ ││  :8080  ││        │
│  │ └───────────┘ │ │└─────────┘│ │└─────────┘│        │
│  └───────────────┘ └───────────┘ └───────────┘         │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │      StatefulSet: Redis (Persistent Storage)       │ │
│  │           Service: redis-service:6379               │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  HPA: Auto-scale Pods (3-10) based on CPU/Memory       │
│  ConfigMaps: Configuration Management                   │
│  Secrets: Redis passwords, API keys                    │
└─────────────────────────────────────────────────────────┘
"""

if __name__ == "__main__":
    print("System Architecture Diagram")
    print("=" * 70)
    print(SYSTEM_ARCHITECTURE)
    print("\n\n")
    print("Request Flow Diagram")
    print("=" * 70)
    print(REQUEST_FLOW)
    print("\n\n")
    print("Data Flow Diagram")
    print("=" * 70)
    print(DATA_FLOW)
    print("\n\n")
    print("Deployment Architecture")
    print("=" * 70)
    print(DEPLOYMENT_ARCHITECTURE)
