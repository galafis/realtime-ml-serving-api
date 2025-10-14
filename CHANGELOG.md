# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete infrastructure setup with Docker, Kubernetes, and monitoring
- Comprehensive test suite (unit, integration, load tests)
- GitHub Actions CI/CD pipeline
- Detailed API documentation (API.md)
- Architecture documentation (ARCHITECTURE.md)
- Contributing guidelines (CONTRIBUTING.md)
- Makefile for development tasks
- Python client features:
  - `batch_predictor.py` for parallel batch predictions
  - `model_evaluator.py` for model evaluation and drift detection
- Configuration files for server, models, and Redis
- Monitoring setup with Prometheus and Grafana
- Kubernetes manifests (deployment, service, HPA, ingress)
- Docker Compose configuration with multi-container setup
- Comprehensive README with:
  - Full Portuguese translation
  - Troubleshooting section
  - FAQ section
  - Contributing guidelines
  - Best practices
- Trained ML models (iris_classifier, binary_classifier)

### Changed
- Enhanced `.gitignore` with more exclusions
- Updated `requirements.txt` with all dependencies
- Improved README with detailed examples and documentation

### Fixed
- Added missing `go.sum` file for reproducible builds
- Fixed Python client import structure

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Go server with Gin framework
- Redis caching support
- Basic prediction endpoint
- Health check endpoint
- Model listing endpoint
- Metrics endpoint
- Python client library
- Model training script
- Basic Docker support
- MIT License

### Features
- Sub-millisecond prediction latency
- Intelligent Redis-based caching
- CORS support
- Request logging middleware
- Graceful shutdown
- Multiple model support

[Unreleased]: https://github.com/galafis/realtime-ml-serving-api/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/galafis/realtime-ml-serving-api/releases/tag/v1.0.0
