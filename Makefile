# Makefile for Real-Time ML Model Serving API
# Author: Gabriel Demetrios Lafis

.PHONY: all build test clean install lint docker-build docker-up docker-down help

# Variables
SERVER_BINARY=ml-server
SERVER_DIR=./server
CLIENT_DIR=./client
DOCKER_COMPOSE=docker/docker-compose.yml

# Default target
all: install build test

## help: Show this help message
help:
	@echo "Available targets:"
	@echo "  install       - Install dependencies"
	@echo "  build         - Build Go server"
	@echo "  test          - Run all tests"
	@echo "  test-go       - Run Go tests"
	@echo "  test-python   - Run Python tests"
	@echo "  lint          - Run linters"
	@echo "  clean         - Clean build artifacts"
	@echo "  docker-build  - Build Docker images"
	@echo "  docker-up     - Start Docker services"
	@echo "  docker-down   - Stop Docker services"
	@echo "  train-models  - Train ML models"
	@echo "  run           - Run server locally"
	@echo "  benchmark     - Run benchmarks"

## install: Install all dependencies
install: install-go install-python

## install-go: Install Go dependencies
install-go:
	@echo "Installing Go dependencies..."
	cd $(SERVER_DIR) && go mod download
	cd $(SERVER_DIR) && go mod tidy

## install-python: Install Python dependencies
install-python:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

## build: Build Go server
build:
	@echo "Building server..."
	cd $(SERVER_DIR) && go build -o $(SERVER_BINARY) main.go
	@echo "Build complete: $(SERVER_DIR)/$(SERVER_BINARY)"

## test: Run all tests
test: test-go test-python

## test-go: Run Go tests
test-go:
	@echo "Running Go tests..."
	cd $(SERVER_DIR) && go test -v -race -coverprofile=coverage.out ./...
	cd $(SERVER_DIR) && go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report: $(SERVER_DIR)/coverage.html"

## test-python: Run Python tests
test-python:
	@echo "Running Python tests..."
	pytest $(CLIENT_DIR)/ -v --cov=$(CLIENT_DIR) --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

## test-integration: Run integration tests
test-integration:
	@echo "Running integration tests..."
	cd tests && go test -v -tags=integration ./...

## test-load: Run load tests
test-load:
	@echo "Running load tests..."
	cd tests && go test -v -run TestHighLoadStress

## lint: Run linters
lint: lint-go lint-python

## lint-go: Lint Go code
lint-go:
	@echo "Linting Go code..."
	cd $(SERVER_DIR) && gofmt -l -w .
	cd $(SERVER_DIR) && go vet ./...
	@command -v golangci-lint >/dev/null 2>&1 && cd $(SERVER_DIR) && golangci-lint run || echo "golangci-lint not installed, skipping"

## lint-python: Lint Python code
lint-python:
	@echo "Linting Python code..."
	@command -v black >/dev/null 2>&1 && black $(CLIENT_DIR)/ || echo "black not installed, skipping"
	@command -v isort >/dev/null 2>&1 && isort $(CLIENT_DIR)/ || echo "isort not installed, skipping"
	@command -v flake8 >/dev/null 2>&1 && flake8 $(CLIENT_DIR)/ --max-line-length=100 || echo "flake8 not installed, skipping"

## clean: Clean build artifacts
clean:
	@echo "Cleaning..."
	rm -f $(SERVER_DIR)/$(SERVER_BINARY)
	rm -f $(SERVER_DIR)/coverage.out
	rm -f $(SERVER_DIR)/coverage.html
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf $(CLIENT_DIR)/__pycache__/
	rm -rf $(CLIENT_DIR)/*.pyc
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete"

## docker-build: Build Docker images
docker-build:
	@echo "Building Docker images..."
	docker-compose -f $(DOCKER_COMPOSE) build

## docker-up: Start Docker services
docker-up:
	@echo "Starting Docker services..."
	docker-compose -f $(DOCKER_COMPOSE) up -d
	@echo "Services started. Check with: docker-compose ps"

## docker-down: Stop Docker services
docker-down:
	@echo "Stopping Docker services..."
	docker-compose -f $(DOCKER_COMPOSE) down

## docker-logs: View Docker logs
docker-logs:
	docker-compose -f $(DOCKER_COMPOSE) logs -f

## train-models: Train ML models
train-models:
	@echo "Training models..."
	cd $(CLIENT_DIR) && python train_model.py
	@echo "Models trained successfully"

## run: Run server locally
run: build
	@echo "Starting server..."
	cd $(SERVER_DIR) && ./$(SERVER_BINARY)

## run-dev: Run server in development mode
run-dev:
	@echo "Starting server in development mode..."
	cd $(SERVER_DIR) && GIN_MODE=debug LOG_LEVEL=debug go run main.go

## benchmark: Run benchmarks
benchmark:
	@echo "Running benchmarks..."
	cd tests && go test -bench=. -benchmem

## deps-update: Update dependencies
deps-update:
	@echo "Updating Go dependencies..."
	cd $(SERVER_DIR) && go get -u ./...
	cd $(SERVER_DIR) && go mod tidy
	@echo "Updating Python dependencies..."
	pip list --outdated

## format: Format all code
format: lint-go lint-python

## check: Run all checks (lint + test)
check: lint test
	@echo "All checks passed!"

## redis-start: Start Redis locally
redis-start:
	docker run -d --name ml-redis -p 6379:6379 redis:7-alpine

## redis-stop: Stop Redis
redis-stop:
	docker stop ml-redis
	docker rm ml-redis

## redis-cli: Connect to Redis CLI
redis-cli:
	docker exec -it ml-redis redis-cli

## k8s-deploy: Deploy to Kubernetes
k8s-deploy:
	@echo "Deploying to Kubernetes..."
	kubectl apply -f kubernetes/

## k8s-delete: Delete from Kubernetes
k8s-delete:
	@echo "Deleting from Kubernetes..."
	kubectl delete -f kubernetes/

## version: Show version information
version:
	@echo "Go version:"
	@go version
	@echo "\nPython version:"
	@python3 --version
	@echo "\nRedis version:"
	@redis-cli --version || echo "Redis not installed locally"
