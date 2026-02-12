# 🤖 Realtime Ml Serving Api

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![MLflow](https://img.shields.io/badge/MLflow-2.10-0194E2.svg)](https://mlflow.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)](https://redis.io/)
[![scikit-learn](https://img.shields.io/badge/scikit-learn-1.4-F7931E.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](#english) | [Português](#português)

---

## English

### 🎯 Overview

**Realtime Ml Serving Api** — High-performance ML model serving API built with Go and Python, featuring Redis caching, model drift monitoring, A/B testing, and MLflow integration

Total source lines: **2,303** across **11** files in **3** languages.

### ✨ Key Features

- **Production-Ready Architecture**: Modular, well-documented, and following best practices
- **Comprehensive Implementation**: Complete solution with all core functionality
- **Clean Code**: Type-safe, well-tested, and maintainable codebase
- **Easy Deployment**: Docker support for quick setup and deployment

### 🚀 Quick Start

#### Prerequisites
- Python 3.12+
- Docker and Docker Compose (optional)

#### Installation

1. **Clone the repository**
```bash
git clone https://github.com/galafis/realtime-ml-serving-api.git
cd realtime-ml-serving-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Running

```bash
python server/main.go
```

## 🐳 Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html

# Run with verbose output
pytest -v
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
├── config/
│   ├── models.yaml
│   ├── redis.yaml
│   └── server.yaml
├── docker/
│   └── docker-compose.yml
├── docs/
│   ├── README.md
│   └── architecture_diagrams.py
├── kubernetes/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── pvc.yaml
│   └── service.yaml
├── models/
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
└── CHANGELOG.md
```

### 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python | 6 files |
| Go | 4 files |
| Shell | 1 files |

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👤 Author

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

---

## Português

### 🎯 Visão Geral

**Realtime Ml Serving Api** — High-performance ML model serving API built with Go and Python, featuring Redis caching, model drift monitoring, A/B testing, and MLflow integration

Total de linhas de código: **2,303** em **11** arquivos em **3** linguagens.

### ✨ Funcionalidades Principais

- **Arquitetura Pronta para Produção**: Modular, bem documentada e seguindo boas práticas
- **Implementação Completa**: Solução completa com todas as funcionalidades principais
- **Código Limpo**: Type-safe, bem testado e manutenível
- **Fácil Implantação**: Suporte Docker para configuração e implantação rápidas

### 🚀 Início Rápido

#### Pré-requisitos
- Python 3.12+
- Docker e Docker Compose (opcional)

#### Instalação

1. **Clone the repository**
```bash
git clone https://github.com/galafis/realtime-ml-serving-api.git
cd realtime-ml-serving-api
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Execução

```bash
python server/main.go
```

### 🧪 Testes

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov --cov-report=html

# Run with verbose output
pytest -v
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
├── config/
│   ├── models.yaml
│   ├── redis.yaml
│   └── server.yaml
├── docker/
│   └── docker-compose.yml
├── docs/
│   ├── README.md
│   └── architecture_diagrams.py
├── kubernetes/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── pvc.yaml
│   └── service.yaml
├── models/
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
└── CHANGELOG.md
```

### 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| Python | 6 files |
| Go | 4 files |
| Shell | 1 files |

### 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 👤 Autor

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)
