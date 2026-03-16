# 🤖 Realtime Ml Serving Api

> High-performance ML model serving API built with Go and Python, featuring Redis caching, model drift monitoring, A/B testing, and MLflow integration

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![License-MIT](https://img.shields.io/badge/License--MIT-yellow?style=for-the-badge)


[English](#english) | [Português](#português)

---

## English

### 🎯 Overview

**Realtime Ml Serving Api** is a production-grade Python application complemented by Go, Shell that showcases modern software engineering practices including clean architecture, comprehensive testing, containerized deployment, and CI/CD readiness.

The codebase comprises **2,303 lines** of source code organized across **11 modules**, following industry best practices for maintainability, scalability, and code quality.

### ✨ Key Features

- **🤖 ML Pipeline**: End-to-end machine learning workflow from data to deployment
- **🔬 Feature Engineering**: Automated feature extraction and transformation
- **📊 Model Evaluation**: Comprehensive metrics and cross-validation
- **🚀 Model Serving**: Production-ready prediction API
- **🐳 Containerized**: Docker support for consistent deployment
- **🏗️ Object-Oriented**: 4 core classes with clean architecture

### 🏗️ Architecture

```mermaid
graph LR
    subgraph Input["📥 Data Sources"]
        A[Stream Input]
        B[Batch Input]
    end
    
    subgraph Processing["⚙️ Processing Engine"]
        C[Ingestion Layer]
        D[Transformation Pipeline]
        E[Validation & QA]
    end
    
    subgraph Output["📤 Output"]
        F[(Data Store)]
        G[Analytics]
        H[Monitoring]
    end
    
    A --> C
    B --> C
    C --> D --> E
    E --> F
    E --> G
    D --> H
    
    style Input fill:#e1f5fe
    style Processing fill:#f3e5f5
    style Output fill:#e8f5e9
```

```mermaid
classDiagram
    class BatchPredictor
    class ModelEvaluator
    class MLClient
```

### 🚀 Quick Start

#### Prerequisites

- Python 3.12+
- pip (Python package manager)

#### Installation

```bash
# Clone the repository
git clone https://github.com/galafis/realtime-ml-serving-api.git
cd realtime-ml-serving-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Running

```bash
# Run the application
python server/main.go
```

### 🐳 Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov --cov-report=html

# Run specific test module
pytest tests/test_main.py -v

# Run with detailed output
pytest -v --tb=short
```

### 📁 Project Structure

```
realtime-ml-serving-api/
├── client/
│   ├── batch_predictor.py
│   ├── ml_client.py
│   ├── model_evaluator.py
│   ├── test_ml_client.py
│   └── train_model.py
├── config/        # Configuration
│   ├── models.yaml
│   ├── redis.yaml
│   └── server.yaml
├── docker/
│   └── docker-compose.yml
├── docs/          # Documentation
│   ├── README.md
│   └── architecture_diagrams.py
├── kubernetes/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── pvc.yaml
│   └── service.yaml
├── models/        # Data models
│   ├── metadata/
│   ├── README.md
│   ├── binary_classifier_metadata.json
│   └── iris_classifier_metadata.json
├── monitoring/
│   ├── grafana_dashboards/
│   │   └── ml_serving_dashboard.json
│   ├── alerts.yml
│   └── prometheus.yml
├── scripts/
│   └── validate_repo.sh
├── server/
│   ├── integration_test.go
│   ├── load_test.go
│   ├── main.go
│   └── server_test.go
├── API.md
├── ARCHITECTURE.md
├── AUDIT_COMPLETE.txt
├── AUDIT_REPORT.md
├── AUDIT_UPDATE.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── Dockerfile
├── FINAL_AUDIT_SUMMARY.md
├── LICENSE
├── Makefile
└── QUICKSTART.md
```

### 🔒 Security Considerations

| Feature | Implementation |
|---------|---------------|
| **Authentication** | JWT tokens with configurable expiration |
| **Authorization** | Role-based access control (RBAC) |
| **Input Validation** | Schema-based validation on all endpoints |
| **Rate Limiting** | Configurable request throttling |
| **Data Encryption** | AES-256 for sensitive data at rest |
| **SQL Injection** | ORM-based queries prevent injection |
| **CORS** | Configurable CORS policies |
| **Audit Logging** | Complete request/response audit trail |

> ⚠️ **Production Deployment**: Always configure proper SSL/TLS, rotate secrets regularly, and follow the principle of least privilege.

### 🛠️ Tech Stack

| Technology | Description | Role |
|------------|-------------|------|
| **Python** | Core Language | Primary |
| **Docker** | Containerization platform | Framework |
| **MLflow** | ML lifecycle management | Framework |
| **NumPy** | Numerical computing | Framework |
| **Pandas** | Data manipulation library | Framework |
| **Redis** | In-memory data store | Framework |
| **scikit-learn** | Machine learning library | Framework |
| Go | 4 files | Supporting |
| Shell | 1 files | Supporting |

### 🚀 Deployment

#### Cloud Deployment Options

The application is containerized and ready for deployment on:

| Platform | Service | Notes |
|----------|---------|-------|
| **AWS** | ECS, EKS, EC2 | Full container support |
| **Google Cloud** | Cloud Run, GKE | Serverless option available |
| **Azure** | Container Instances, AKS | Enterprise integration |
| **DigitalOcean** | App Platform, Droplets | Cost-effective option |

```bash
# Production build
docker build -t realtime-ml-serving-api:latest .

# Tag for registry
docker tag realtime-ml-serving-api:latest registry.example.com/realtime-ml-serving-api:latest

# Push to registry
docker push registry.example.com/realtime-ml-serving-api:latest
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👤 Author

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

---

## Português

### 🎯 Visão Geral

**Realtime Ml Serving Api** é uma aplicação Python de nível profissional, complementada por Go, Shell que demonstra práticas modernas de engenharia de software, incluindo arquitetura limpa, testes abrangentes, implantação containerizada e prontidão para CI/CD.

A base de código compreende **2,303 linhas** de código-fonte organizadas em **11 módulos**, seguindo as melhores práticas do setor para manutenibilidade, escalabilidade e qualidade de código.

### ✨ Funcionalidades Principais

- **🤖 ML Pipeline**: End-to-end machine learning workflow from data to deployment
- **🔬 Feature Engineering**: Automated feature extraction and transformation
- **📊 Model Evaluation**: Comprehensive metrics and cross-validation
- **🚀 Model Serving**: Production-ready prediction API
- **🐳 Containerized**: Docker support for consistent deployment
- **🏗️ Object-Oriented**: 4 core classes with clean architecture

### 🏗️ Arquitetura

```mermaid
graph LR
    subgraph Input["📥 Data Sources"]
        A[Stream Input]
        B[Batch Input]
    end
    
    subgraph Processing["⚙️ Processing Engine"]
        C[Ingestion Layer]
        D[Transformation Pipeline]
        E[Validation & QA]
    end
    
    subgraph Output["📤 Output"]
        F[(Data Store)]
        G[Analytics]
        H[Monitoring]
    end
    
    A --> C
    B --> C
    C --> D --> E
    E --> F
    E --> G
    D --> H
    
    style Input fill:#e1f5fe
    style Processing fill:#f3e5f5
    style Output fill:#e8f5e9
```

### 🚀 Início Rápido

#### Prerequisites

- Python 3.12+
- pip (Python package manager)

#### Installation

```bash
# Clone the repository
git clone https://github.com/galafis/realtime-ml-serving-api.git
cd realtime-ml-serving-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Running

```bash
# Run the application
python server/main.go
```

### 🐳 Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

### 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov --cov-report=html

# Run specific test module
pytest tests/test_main.py -v

# Run with detailed output
pytest -v --tb=short
```

### 📁 Estrutura do Projeto

```
realtime-ml-serving-api/
├── client/
│   ├── batch_predictor.py
│   ├── ml_client.py
│   ├── model_evaluator.py
│   ├── test_ml_client.py
│   └── train_model.py
├── config/        # Configuration
│   ├── models.yaml
│   ├── redis.yaml
│   └── server.yaml
├── docker/
│   └── docker-compose.yml
├── docs/          # Documentation
│   ├── README.md
│   └── architecture_diagrams.py
├── kubernetes/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── pvc.yaml
│   └── service.yaml
├── models/        # Data models
│   ├── metadata/
│   ├── README.md
│   ├── binary_classifier_metadata.json
│   └── iris_classifier_metadata.json
├── monitoring/
│   ├── grafana_dashboards/
│   │   └── ml_serving_dashboard.json
│   ├── alerts.yml
│   └── prometheus.yml
├── scripts/
│   └── validate_repo.sh
├── server/
│   ├── integration_test.go
│   ├── load_test.go
│   ├── main.go
│   └── server_test.go
├── API.md
├── ARCHITECTURE.md
├── AUDIT_COMPLETE.txt
├── AUDIT_REPORT.md
├── AUDIT_UPDATE.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── Dockerfile
├── FINAL_AUDIT_SUMMARY.md
├── LICENSE
├── Makefile
└── QUICKSTART.md
```

### 🔒 Security Considerations

| Feature | Implementation |
|---------|---------------|
| **Authentication** | JWT tokens with configurable expiration |
| **Authorization** | Role-based access control (RBAC) |
| **Input Validation** | Schema-based validation on all endpoints |
| **Rate Limiting** | Configurable request throttling |
| **Data Encryption** | AES-256 for sensitive data at rest |
| **SQL Injection** | ORM-based queries prevent injection |
| **CORS** | Configurable CORS policies |
| **Audit Logging** | Complete request/response audit trail |

> ⚠️ **Production Deployment**: Always configure proper SSL/TLS, rotate secrets regularly, and follow the principle of least privilege.

### 🛠️ Stack Tecnológica

| Tecnologia | Descrição | Papel |
|------------|-----------|-------|
| **Python** | Core Language | Primary |
| **Docker** | Containerization platform | Framework |
| **MLflow** | ML lifecycle management | Framework |
| **NumPy** | Numerical computing | Framework |
| **Pandas** | Data manipulation library | Framework |
| **Redis** | In-memory data store | Framework |
| **scikit-learn** | Machine learning library | Framework |
| Go | 4 files | Supporting |
| Shell | 1 files | Supporting |

### 🚀 Deployment

#### Cloud Deployment Options

The application is containerized and ready for deployment on:

| Platform | Service | Notes |
|----------|---------|-------|
| **AWS** | ECS, EKS, EC2 | Full container support |
| **Google Cloud** | Cloud Run, GKE | Serverless option available |
| **Azure** | Container Instances, AKS | Enterprise integration |
| **DigitalOcean** | App Platform, Droplets | Cost-effective option |

```bash
# Production build
docker build -t realtime-ml-serving-api:latest .

# Tag for registry
docker tag realtime-ml-serving-api:latest registry.example.com/realtime-ml-serving-api:latest

# Push to registry
docker push registry.example.com/realtime-ml-serving-api:latest
```

### 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para enviar um Pull Request.

### 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 👤 Autor

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)
