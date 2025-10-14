package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
)

// Author: Gabriel Demetrios Lafis

// Load test configuration
type LoadTestConfig struct {
	NumClients         int
	RequestsPerClient  int
	RampUpTime         time.Duration
	TargetEndpoint     string
}

// Load test results
type LoadTestResults struct {
	TotalRequests      int
	SuccessfulRequests int
	FailedRequests     int
	TotalDuration      time.Duration
	AvgLatency         time.Duration
	MinLatency         time.Duration
	MaxLatency         time.Duration
	RequestsPerSecond  float64
	Percentiles        map[int]time.Duration
}

// Run load test
func runLoadTest(t *testing.T, router *gin.Engine, config LoadTestConfig) LoadTestResults {
	var wg sync.WaitGroup
	latencies := make([]time.Duration, 0, config.NumClients*config.RequestsPerClient)
	var latenciesMutex sync.Mutex
	
	successCount := 0
	failCount := 0
	var countMutex sync.Mutex
	
	startTime := time.Now()
	
	// Spawn clients
	for i := 0; i < config.NumClients; i++ {
		wg.Add(1)
		
		go func(clientID int) {
			defer wg.Done()
			
			// Ramp up delay
			if config.RampUpTime > 0 {
				delay := time.Duration(clientID) * (config.RampUpTime / time.Duration(config.NumClients))
				time.Sleep(delay)
			}
			
			// Make requests
			for j := 0; j < config.RequestsPerClient; j++ {
				reqBody := PredictionRequest{
					ModelName: "iris_classifier",
					Features:  []float64{5.1, 3.5, 1.4, 0.2},
				}
				
				bodyBytes, _ := json.Marshal(reqBody)
				req, _ := http.NewRequest("POST", config.TargetEndpoint, bytes.NewBuffer(bodyBytes))
				req.Header.Set("Content-Type", "application/json")
				resp := httptest.NewRecorder()
				
				requestStart := time.Now()
				router.ServeHTTP(resp, req)
				latency := time.Since(requestStart)
				
				latenciesMutex.Lock()
				latencies = append(latencies, latency)
				latenciesMutex.Unlock()
				
				countMutex.Lock()
				if resp.Code == http.StatusOK {
					successCount++
				} else {
					failCount++
				}
				countMutex.Unlock()
			}
		}(i)
	}
	
	wg.Wait()
	totalDuration := time.Since(startTime)
	
	// Calculate statistics
	results := LoadTestResults{
		TotalRequests:      len(latencies),
		SuccessfulRequests: successCount,
		FailedRequests:     failCount,
		TotalDuration:      totalDuration,
		RequestsPerSecond:  float64(len(latencies)) / totalDuration.Seconds(),
		Percentiles:        make(map[int]time.Duration),
	}
	
	if len(latencies) > 0 {
		// Sort latencies for percentile calculation
		// Simple insertion sort for small arrays
		for i := 1; i < len(latencies); i++ {
			key := latencies[i]
			j := i - 1
			for j >= 0 && latencies[j] > key {
				latencies[j+1] = latencies[j]
				j--
			}
			latencies[j+1] = key
		}
		
		// Calculate metrics
		var totalLatency time.Duration
		for _, l := range latencies {
			totalLatency += l
		}
		results.AvgLatency = totalLatency / time.Duration(len(latencies))
		results.MinLatency = latencies[0]
		results.MaxLatency = latencies[len(latencies)-1]
		
		// Calculate percentiles
		percentiles := []int{50, 75, 90, 95, 99}
		for _, p := range percentiles {
			index := (len(latencies) * p) / 100
			if index >= len(latencies) {
				index = len(latencies) - 1
			}
			results.Percentiles[p] = latencies[index]
		}
	}
	
	return results
}

// Print load test results
func printLoadTestResults(t *testing.T, results LoadTestResults) {
	t.Logf("\n" + "=".repeat(60))
	t.Logf("Load Test Results")
	t.Logf("=".repeat(60))
	t.Logf("Total Requests:      %d", results.TotalRequests)
	t.Logf("Successful:          %d", results.SuccessfulRequests)
	t.Logf("Failed:              %d", results.FailedRequests)
	t.Logf("Total Duration:      %v", results.TotalDuration)
	t.Logf("Throughput:          %.0f req/s", results.RequestsPerSecond)
	t.Logf("\nLatency Statistics:")
	t.Logf("  Average:           %v", results.AvgLatency)
	t.Logf("  Min:               %v", results.MinLatency)
	t.Logf("  Max:               %v", results.MaxLatency)
	t.Logf("\nPercentiles:")
	for _, p := range []int{50, 75, 90, 95, 99} {
		if latency, ok := results.Percentiles[p]; ok {
			t.Logf("  P%d:              %v", p, latency)
		}
	}
	t.Logf("=".repeat(60))
}

// Helper function for string repeat
func (s string) repeat(count int) string {
	result := ""
	for i := 0; i < count; i++ {
		result += "="
	}
	return result
}

// Test: Light load
func TestLightLoad(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping load test in short mode")
	}
	
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	router.POST("/predict", predict)
	
	config := LoadTestConfig{
		NumClients:        10,
		RequestsPerClient: 100,
		RampUpTime:        time.Second,
		TargetEndpoint:    "/predict",
	}
	
	results := runLoadTest(t, router, config)
	printLoadTestResults(t, results)
	
	// Assertions
	if results.FailedRequests > 0 {
		t.Errorf("Expected 0 failed requests, got %d", results.FailedRequests)
	}
	if results.AvgLatency > 10*time.Millisecond {
		t.Errorf("Average latency too high: %v", results.AvgLatency)
	}
}

// Test: Medium load
func TestMediumLoad(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping load test in short mode")
	}
	
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	router.POST("/predict", predict)
	
	config := LoadTestConfig{
		NumClients:        50,
		RequestsPerClient: 100,
		RampUpTime:        2 * time.Second,
		TargetEndpoint:    "/predict",
	}
	
	results := runLoadTest(t, router, config)
	printLoadTestResults(t, results)
	
	// Should handle 5000 requests
	if results.SuccessfulRequests < 4900 {
		t.Errorf("Too many failed requests: %d", results.FailedRequests)
	}
}

// Test: High load stress test
func TestHighLoadStress(t *testing.T) {
	if testing.Short() {
		t.Skip("Skipping load test in short mode")
	}
	
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	router.POST("/predict", predict)
	
	config := LoadTestConfig{
		NumClients:        100,
		RequestsPerClient: 100,
		RampUpTime:        3 * time.Second,
		TargetEndpoint:    "/predict",
	}
	
	results := runLoadTest(t, router, config)
	printLoadTestResults(t, results)
	
	t.Logf("Error rate: %.2f%%", float64(results.FailedRequests)/float64(results.TotalRequests)*100)
}

// Benchmark prediction endpoint
func BenchmarkPredictEndpoint(b *testing.B) {
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	router.POST("/predict", predict)
	
	reqBody := PredictionRequest{
		ModelName: "iris_classifier",
		Features:  []float64{5.1, 3.5, 1.4, 0.2},
	}
	bodyBytes, _ := json.Marshal(reqBody)
	
	b.ResetTimer()
	
	for i := 0; i < b.N; i++ {
		req, _ := http.NewRequest("POST", "/predict", bytes.NewBuffer(bodyBytes))
		req.Header.Set("Content-Type", "application/json")
		resp := httptest.NewRecorder()
		router.ServeHTTP(resp, req)
	}
}

// Helper to repeat strings (since strings package doesn't have Repeat in older Go)
func repeatString(s string, count int) string {
	var result string
	for i := 0; i < count; i++ {
		result += s
	}
	return result
}
