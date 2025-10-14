#!/bin/bash
# Repository Validation Script
# Author: Gabriel Demetrios Lafis
# This script validates the repository setup

set -e  # Exit on error

echo "================================"
echo "Repository Validation Script"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0

# Check function
check() {
    local test_name="$1"
    local command="$2"
    
    echo -n "Checking $test_name... "
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
        return 1
    fi
}

echo "1. Checking Repository Structure"
echo "================================"
check "server directory" "test -d server"
check "client directory" "test -d client"
check "config directory" "test -d config"
check "docker directory" "test -d docker"
check "kubernetes directory" "test -d kubernetes"
check "models directory" "test -d models"
check "monitoring directory" "test -d monitoring"
check "docs directory" "test -d docs"
echo ""

echo "2. Checking Core Files"
echo "================================"
check "README.md" "test -f README.md"
check "LICENSE" "test -f LICENSE"
check "Makefile" "test -f Makefile"
check "requirements.txt" "test -f requirements.txt"
check ".env.example" "test -f .env.example"
check "CONTRIBUTING.md" "test -f CONTRIBUTING.md"
check "CHANGELOG.md" "test -f CHANGELOG.md"
check "ARCHITECTURE.md" "test -f ARCHITECTURE.md"
check "API.md" "test -f API.md"
echo ""

echo "3. Checking Server Files"
echo "================================"
check "server/main.go" "test -f server/main.go"
check "server/go.mod" "test -f server/go.mod"
check "server/go.sum" "test -f server/go.sum"
check "server tests" "test -f server/server_test.go && test -f server/integration_test.go && test -f server/load_test.go"
echo ""

echo "4. Checking Client Files"
echo "================================"
check "client/ml_client.py" "test -f client/ml_client.py"
check "client/train_model.py" "test -f client/train_model.py"
check "client/model_evaluator.py" "test -f client/model_evaluator.py"
check "client/batch_predictor.py" "test -f client/batch_predictor.py"
check "client/test_ml_client.py" "test -f client/test_ml_client.py"
echo ""

echo "5. Checking Documentation"
echo "================================"
check "docs/README.md" "test -f docs/README.md"
check "docs/architecture_diagrams.py" "test -f docs/architecture_diagrams.py"
check "AUDIT_UPDATE.md" "test -f AUDIT_UPDATE.md"
check "QUICKSTART.md" "test -f QUICKSTART.md"
echo ""

echo "6. Checking Configuration Files"
echo "================================"
check "config/server.yaml" "test -f config/server.yaml"
check "config/redis.yaml" "test -f config/redis.yaml"
check "config/models.yaml" "test -f config/models.yaml"
echo ""

echo "7. Checking Docker Files"
echo "================================"
check "Dockerfile.server" "test -f docker/Dockerfile.server"
check "Dockerfile.client" "test -f docker/Dockerfile.client"
check "docker-compose.yml" "test -f docker/docker-compose.yml"
echo ""

echo "8. Checking Kubernetes Files"
echo "================================"
check "deployment.yaml" "test -f kubernetes/deployment.yaml"
check "service.yaml" "test -f kubernetes/service.yaml"
check "hpa.yaml" "test -f kubernetes/hpa.yaml"
check "ingress.yaml" "test -f kubernetes/ingress.yaml"
echo ""

echo "9. Checking Go Code"
echo "================================"
if command -v go &> /dev/null; then
    check "Go installed" "go version"
    check "Go build" "cd server && go build -o /tmp/ml-server-test main.go && rm /tmp/ml-server-test"
    check "Go format" "cd server && gofmt -l . | wc -l | grep -q '^0$'"
    check "Go vet" "cd server && go vet ./..."
else
    echo -e "${YELLOW}⚠ WARNING: Go not installed, skipping Go checks${NC}"
fi
echo ""

echo "10. Checking Python Code"
echo "================================"
if command -v python3 &> /dev/null; then
    check "Python installed" "python3 --version"
    check "Python syntax (client)" "python3 -m py_compile client/*.py"
    check "Python syntax (docs)" "python3 -m py_compile docs/*.py"
else
    echo -e "${YELLOW}⚠ WARNING: Python not installed, skipping Python checks${NC}"
fi
echo ""

echo "================================"
echo "Validation Summary"
echo "================================"
echo -e "Tests Passed: ${GREEN}$PASSED${NC}"
echo -e "Tests Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! Repository is in good condition.${NC}"
    exit 0
else
    echo -e "${RED}✗ Some checks failed. Please review the errors above.${NC}"
    exit 1
fi
