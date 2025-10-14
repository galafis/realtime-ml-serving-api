# 🧪 Testing Guide

Complete guide for running and understanding tests in the Real-Time ML Model Serving API.

---

## Quick Start

```bash
# Run all tests
make test

# Or manually
cd server && go test -v ./...
```

---

## Test Structure

All tests are located in the `server/` directory:

```
server/
├── main.go                # Application code
├── server_test.go         # Unit tests
├── integration_test.go    # Integration tests
└── load_test.go          # Load/performance tests
```

---

## Running Tests

### All Tests

```bash
# Using Makefile (recommended)
make test

# Manual
cd server
go test -v ./...
```

### Unit Tests Only

```bash
cd server
go test -v -run Test -short
```

### Integration Tests

```bash
# Includes API flow testing
cd server
go test -v -run TestIntegration
```

### Load Tests

```bash
# Warning: These tests are resource intensive and skipped by default
cd server
go test -v -run TestLoad
```

### Specific Test

```bash
cd server
go test -v -run TestHealthCheck
```

---

## Test Coverage

### Generate Coverage Report

```bash
cd server
go test -race -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html
```

View `coverage.html` in your browser.

### Quick Coverage Summary

```bash
cd server
go test -cover ./...
```

---

## Test Descriptions

### Unit Tests (server_test.go)

#### TestHealthCheck
- **Purpose:** Validates health check endpoint
- **Duration:** < 1ms
- **Checks:**
  - Returns HTTP 200
  - Response has correct status field
  - Version information included

#### TestPredictEndpoint
- **Purpose:** Tests prediction endpoint with valid/invalid requests
- **Duration:** ~160ms (first prediction, no cache)
- **Checks:**
  - Valid requests return predictions
  - Invalid requests return 400 Bad Request
  - Response includes latency metrics

#### TestListModels
- **Purpose:** Validates model listing endpoint
- **Duration:** < 1ms
- **Checks:**
  - Returns list of available models
  - Count matches number of models
  - Model metadata included

#### TestGetMetrics
- **Purpose:** Tests metrics endpoint
- **Duration:** < 1ms
- **Checks:**
  - Returns API metrics
  - Includes request count, latency, cache hit rate

#### TestCORSMiddleware
- **Purpose:** Validates CORS headers
- **Duration:** < 1ms
- **Checks:**
  - CORS headers present
  - Allowed origins configured
  - OPTIONS requests handled

#### TestMakePrediction
- **Purpose:** Tests prediction logic directly
- **Duration:** < 1ms
- **Checks:**
  - Correct classification (sum < 10 → 0, sum > 10 → 1)
  - Probability values returned

### Integration Tests (integration_test.go)

#### TestIntegrationPredictionFlow
- **Purpose:** End-to-end API workflow test
- **Duration:** ~330ms
- **Checks:**
  - Health check → List models → Predict → Get metrics
  - Multiple model predictions
  - Response format validation

#### TestConcurrentPredictions
- **Purpose:** Tests concurrent request handling
- **Duration:** ~16s
- **Checks:**
  - 100 concurrent predictions
  - No race conditions
  - All requests succeed

#### TestAPIPerformance
- **Purpose:** Performance benchmarking
- **Duration:** ~17.5s
- **Checks:**
  - Average latency < 200ms (without Redis)
  - Consistent performance across requests

### Load Tests (load_test.go)

#### TestLightLoad
- **Purpose:** Light load test (1,000 requests)
- **Config:**
  - 10 concurrent clients
  - 100 requests per client
  - 1s ramp-up
- **Skipped in:** Short mode (`-short` flag)

#### TestMediumLoad
- **Purpose:** Medium load test (5,000 requests)
- **Config:**
  - 50 concurrent clients
  - 100 requests per client
  - 2s ramp-up
- **Skipped in:** Short mode

#### TestHighLoadStress
- **Purpose:** High load stress test (10,000 requests)
- **Config:**
  - 100 concurrent clients
  - 100 requests per client
  - 3s ramp-up
- **Skipped in:** Short mode

---

## Test Modes

### Short Mode (Default for CI)

Skips long-running tests:

```bash
go test -v -short ./...
```

### Full Mode

Runs all tests including load tests:

```bash
go test -v ./...
```

**Warning:** Full mode can take several minutes and is resource-intensive.

---

## Python Tests

### Location

```
client/
└── test_ml_client.py
```

### Running Python Tests

```bash
# Using pytest
pytest client/test_ml_client.py -v

# With coverage
pytest client/ -v --cov=client --cov-report=html

# Using Makefile
make test-python
```

### Python Test Cases

- Client initialization
- Custom URL configuration
- Method existence checks
- Module imports

---

## Performance Expectations

### Without Redis Cache (Test Environment)

| Metric | Expected Value |
|--------|----------------|
| Health Check | < 1ms |
| First Prediction | ~160ms |
| Subsequent Predictions | ~160ms (no cache) |
| Model List | < 1ms |
| Metrics | < 1ms |
| Concurrent Requests | 100+ simultaneous |

### With Redis Cache (Production)

| Metric | Expected Value |
|--------|----------------|
| Cached Prediction | < 1ms |
| Cache Hit Rate | 85-95% |
| P50 Latency | < 1ms |
| P99 Latency | < 5ms |
| Throughput | 50,000+ req/sec |

---

## Troubleshooting Tests

### Redis Connection Errors

If you see `Redis connection failed` warnings:

```bash
# This is expected in tests - Redis is optional
# Tests will still pass without Redis

# To enable Redis for tests:
docker run -d -p 6379:6379 redis:latest
```

### Race Condition Errors

Tests use `-race` flag to detect race conditions:

```bash
# If race conditions are found:
cd server
go test -race ./...

# The output will show the exact location
```

### Timeout Errors

For slow systems, increase test timeout:

```bash
cd server
go test -v -timeout 5m ./...
```

### Port Already in Use

If port 8080 is in use:

```bash
# Find and kill the process
lsof -i :8080
kill -9 <PID>

# Or use a different port (modify code)
```

---

## CI/CD Integration

### GitHub Actions

Tests run automatically on:
- Push to main/master/develop
- Pull requests
- Manual workflow dispatch

Configuration: `.github/workflows/ci.yml`

### Local CI Simulation

```bash
# Run what CI runs
make test
make lint
make build
```

---

## Writing New Tests

### Test Structure

```go
func TestMyFeature(t *testing.T) {
    gin.SetMode(gin.TestMode)
    
    // Setup
    router := gin.Default()
    router.GET("/endpoint", myHandler)
    
    // Test
    req, _ := http.NewRequest("GET", "/endpoint", nil)
    resp := httptest.NewRecorder()
    router.ServeHTTP(resp, req)
    
    // Assert
    assert.Equal(t, http.StatusOK, resp.Code)
}
```

### Test Naming Convention

- Start with `Test`
- Use descriptive names
- Use subtests with `t.Run()`

```go
func TestFeature(t *testing.T) {
    t.Run("Success case", func(t *testing.T) {
        // test code
    })
    
    t.Run("Error case", func(t *testing.T) {
        // test code
    })
}
```

---

## Benchmarking

### Run Benchmarks

```bash
cd server
go test -bench=. -benchmem
```

### Example Benchmark

```go
func BenchmarkPrediction(b *testing.B) {
    features := []float64{5.1, 3.5, 1.4, 0.2}
    
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        makePrediction(features)
    }
}
```

---

## Best Practices

1. **Always run tests before committing**
   ```bash
   make test
   ```

2. **Check code coverage**
   ```bash
   make test-go  # Generates coverage.html
   ```

3. **Test in CI environment**
   - Push to a feature branch
   - Verify CI passes

4. **Run load tests before production**
   ```bash
   cd server
   go test -v -run TestHighLoadStress
   ```

5. **Use table-driven tests** for multiple scenarios
   ```go
   testCases := []struct {
       name     string
       input    []float64
       expected int
   }{
       {"Case 1", []float64{1,2,3}, 0},
       {"Case 2", []float64{5,5,5}, 1},
   }
   
   for _, tc := range testCases {
       t.Run(tc.name, func(t *testing.T) {
           // test code
       })
   }
   ```

---

## Test Maintenance

### When to Update Tests

- After changing API endpoints
- After modifying response formats
- After adding new features
- After fixing bugs (add regression tests)

### Keeping Tests Fast

- Mock external dependencies
- Use test fixtures
- Avoid unnecessary setup
- Run heavy tests in separate mode

---

## Resources

- [Go Testing Package](https://pkg.go.dev/testing)
- [Testify Documentation](https://github.com/stretchr/testify)
- [Gin Testing Guide](https://gin-gonic.com/docs/testing/)
- [pytest Documentation](https://docs.pytest.org/)

---

## Summary

**Current Test Status:**
- ✅ 8 Go tests passing
- ✅ 100% pass rate
- ✅ ~18s execution time
- ✅ Race detection enabled
- ✅ Coverage reporting available

**Quick Commands:**
```bash
make test           # Run all tests
make test-go        # Go tests with coverage
make test-python    # Python tests
make lint           # Lint code
```

---

**Questions?** See [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue.
