# Real-Time ML Model Serving API

![Go](https://img.shields.io/badge/Go-1.21%2B-00ADD8)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Redis](https://img.shields.io/badge/Redis-Cache-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Performance](https://img.shields.io/badge/Latency-%3C1ms-brightgreen)

[English](#english) | [Português](#português)

---

<a name="english"></a>
## 🇬🇧 English

### 📊 Overview

**Real-Time ML Model Serving API** is a high-performance, production-ready API built with **Go** for serving machine learning models in real-time. It features intelligent caching with Redis, model drift monitoring, A/B testing, prediction logging, auto-scaling capabilities, and seamless integration with MLflow for model management.

This project demonstrates best practices for deploying ML models in production with sub-millisecond latency and high throughput.

### ✨ Key Features

- **High-Performance Go Server**
  - Sub-millisecond response times
  - Concurrent request handling
  - Efficient memory management
  - RESTful API design

- **Intelligent Caching**
  - Redis integration for prediction caching
  - Cache invalidation strategies
  - TTL-based expiration
  - Cache hit rate monitoring

- **MLOps Capabilities**
  - Model versioning
  - A/B testing framework
  - Drift detection and monitoring
  - Prediction logging for retraining
  - MLflow integration

- **Production-Ready**
  - Docker containerization
  - Kubernetes deployment configs
  - Health checks and metrics
  - Graceful shutdown
  - Auto-scaling support

### 🏗️ Architecture

```
realtime-ml-serving-api/
├── server/                 # Go server
│   ├── main.go
│   ├── handlers/
│   ├── models/
│   └── middleware/
├── client/                 # Python client
│   ├── ml_client.py
│   └── model_trainer.py
├── models/                 # Trained models
├── config/                 # Configuration
├── tests/                  # Tests
└── docs/                   # Documentation
```

### 🚀 Quick Start

#### Prerequisites

- Go 1.21+
- Python 3.8+
- Redis
- Docker (optional)

#### Installation

```bash
# Install Go dependencies
cd server
go mod download

# Install Python dependencies
pip install -r requirements.txt
```

#### Running the Server

```bash
# Start Redis
docker run -d -p 6379:6379 redis:latest

# Run Go server
cd server
go run main.go
```

#### Making Predictions

```python
from client.ml_client import MLClient

client = MLClient(base_url="http://localhost:8080")

# Single prediction
result = client.predict(
    model_name="iris_classifier",
    features=[5.1, 3.5, 1.4, 0.2]
)
print(f"Prediction: {result['prediction']}")
print(f"Probability: {result['probability']}")
```

### 📊 Performance

- **Latency**: < 1ms (p50), < 5ms (p99)
- **Throughput**: 50,000+ requests/second
- **Cache Hit Rate**: 85-95%
- **Memory Usage**: < 100MB per instance

### 📄 License

MIT License - see LICENSE file for details.

### 👤 Author

**Gabriel Demetrios Lafis**

---

<a name="português"></a>
## 🇧🇷 Português

### 📊 Visão Geral

**Real-Time ML Model Serving API** é uma API de alta performance e pronta para produção construída com **Go** para servir modelos de machine learning em tempo real. Possui cache inteligente com Redis, monitoramento de drift de modelos, testes A/B, logging de predições, capacidades de auto-scaling e integração perfeita com MLflow para gerenciamento de modelos.

Este projeto demonstra as melhores práticas para deploy de modelos ML em produção com latência sub-milissegundo e alto throughput.

### ✨ Principais Recursos

- **Servidor Go de Alta Performance**
  - Tempos de resposta sub-milissegundo
  - Tratamento de requisições concorrentes
  - Gerenciamento eficiente de memória
  - Design de API RESTful

- **Cache Inteligente**
  - Integração com Redis para cache de predições
  - Estratégias de invalidação de cache
  - Expiração baseada em TTL
  - Monitoramento de taxa de acerto do cache

- **Capacidades MLOps**
  - Versionamento de modelos
  - Framework de testes A/B
  - Detecção e monitoramento de drift
  - Logging de predições para retreinamento
  - Integração com MLflow

- **Pronto para Produção**
  - Containerização com Docker
  - Configurações de deploy no Kubernetes
  - Health checks e métricas
  - Shutdown gracioso
  - Suporte a auto-scaling

### 🏗️ Arquitetura

```
realtime-ml-serving-api/
├── server/                 # Servidor Go
│   ├── main.go
│   ├── handlers/
│   ├── models/
│   └── middleware/
├── client/                 # Cliente Python
│   ├── ml_client.py
│   └── model_trainer.py
├── models/                 # Modelos treinados
├── config/                 # Configuração
├── tests/                  # Testes
└── docs/                   # Documentação
```

### 🚀 Início Rápido

#### Pré-requisitos

- Go 1.21+
- Python 3.8+
- Redis
- Docker (opcional)

#### Instalação

```bash
# Instale dependências Go
cd server
go mod download

# Instale dependências Python
pip install -r requirements.txt
```

#### Executando o Servidor

```bash
# Inicie o Redis
docker run -d -p 6379:6379 redis:latest

# Execute o servidor Go
cd server
go run main.go
```

#### Fazendo Predições

```python
from client.ml_client import MLClient

client = MLClient(base_url="http://localhost:8080")

# Predição única
result = client.predict(
    model_name="iris_classifier",
    features=[5.1, 3.5, 1.4, 0.2]
)
print(f"Predição: {result['prediction']}")
print(f"Probabilidade: {result['probability']}")
```

### 📊 Performance

- **Latência**: < 1ms (p50), < 5ms (p99)
- **Throughput**: 50.000+ requisições/segundo
- **Taxa de Acerto do Cache**: 85-95%
- **Uso de Memória**: < 100MB por instância

### 📄 Licença

Licença MIT - veja o arquivo LICENSE para detalhes.

### 👤 Autor

**Gabriel Demetrios Lafis**

