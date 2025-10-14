package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

// Author: Gabriel Demetrios Lafis

// Integration test for complete prediction flow
func TestIntegrationPredictionFlow(t *testing.T) {
	gin.SetMode(gin.TestMode)
	
	router := gin.Default()
	router.Use(corsMiddleware())
	router.Use(metricsMiddleware())
	router.GET("/health", healthCheck)
	router.POST("/predict", predict)
	router.GET("/models", listModels)
	router.GET("/metrics", getMetrics)
	
	// 1. Test health check
	t.Run("Health check", func(t *testing.T) {
		req, _ := http.NewRequest("GET", "/health", nil)
		resp := httptest.NewRecorder()
		router.ServeHTTP(resp, req)
		
		assert.Equal(t, http.StatusOK, resp.Code)
	})
	
	// 2. Test list models
	t.Run("List available models", func(t *testing.T) {
		req, _ := http.NewRequest("GET", "/models", nil)
		resp := httptest.NewRecorder()
		router.ServeHTTP(resp, req)
		
		assert.Equal(t, http.StatusOK, resp.Code)
		
		var result map[string]interface{}
		json.Unmarshal(resp.Body.Bytes(), &result)
		assert.Greater(t, result["count"], 0.0)
	})
	
	// 3. Test predictions
	t.Run("Make predictions", func(t *testing.T) {
		testCases := []struct {
			name     string
			modelName string
			features  []float64
		}{
			{
				name:      "Iris classifier",
				modelName: "iris_classifier",
				features:  []float64{5.1, 3.5, 1.4, 0.2},
			},
			{
				name:      "Fraud detector",
				modelName: "fraud_detector",
				features:  []float64{100.0, 1, 2, 3, 4},
			},
		}
		
		for _, tc := range testCases {
			t.Run(tc.name, func(t *testing.T) {
				reqBody := PredictionRequest{
					ModelName: tc.modelName,
					Features:  tc.features,
				}
				
				bodyBytes, _ := json.Marshal(reqBody)
				req, _ := http.NewRequest("POST", "/predict", bytes.NewBuffer(bodyBytes))
				req.Header.Set("Content-Type", "application/json")
				resp := httptest.NewRecorder()
				
				router.ServeHTTP(resp, req)
				
				assert.Equal(t, http.StatusOK, resp.Code)
				
				var result PredictionResponse
				json.Unmarshal(resp.Body.Bytes(), &result)
				assert.NotNil(t, result.Prediction)
				assert.Equal(t, tc.modelName, result.ModelName)
			})
		}
	})
	
	// 4. Test metrics endpoint
	t.Run("Get metrics", func(t *testing.T) {
		req, _ := http.NewRequest("GET", "/metrics", nil)
		resp := httptest.NewRecorder()
		router.ServeHTTP(resp, req)
		
		assert.Equal(t, http.StatusOK, resp.Code)
	})
}

// Test concurrent predictions
func TestConcurrentPredictions(t *testing.T) {
	gin.SetMode(gin.TestMode)
	
	router := gin.Default()
	router.POST("/predict", predict)
	
	numRequests := 100
	results := make(chan int, numRequests)
	
	for i := 0; i < numRequests; i++ {
		go func() {
			reqBody := PredictionRequest{
				ModelName: "iris_classifier",
				Features:  []float64{5.1, 3.5, 1.4, 0.2},
			}
			
			bodyBytes, _ := json.Marshal(reqBody)
			req, _ := http.NewRequest("POST", "/predict", bytes.NewBuffer(bodyBytes))
			req.Header.Set("Content-Type", "application/json")
			resp := httptest.NewRecorder()
			
			router.ServeHTTP(resp, req)
			results <- resp.Code
		}()
	}
	
	// Collect results
	successCount := 0
	for i := 0; i < numRequests; i++ {
		code := <-results
		if code == http.StatusOK {
			successCount++
		}
	}
	
	assert.Equal(t, numRequests, successCount)
}

// Test API rate and latency
func TestAPIPerformance(t *testing.T) {
	gin.SetMode(gin.TestMode)
	
	router := gin.Default()
	router.POST("/predict", predict)
	
	// Warm up
	for i := 0; i < 10; i++ {
		reqBody := PredictionRequest{
			ModelName: "iris_classifier",
			Features:  []float64{5.1, 3.5, 1.4, 0.2},
		}
		bodyBytes, _ := json.Marshal(reqBody)
		req, _ := http.NewRequest("POST", "/predict", bytes.NewBuffer(bodyBytes))
		req.Header.Set("Content-Type", "application/json")
		resp := httptest.NewRecorder()
		router.ServeHTTP(resp, req)
	}
	
	// Measure latency
	numRequests := 100
	latencies := make([]time.Duration, numRequests)
	
	for i := 0; i < numRequests; i++ {
		reqBody := PredictionRequest{
			ModelName: "iris_classifier",
			Features:  []float64{5.1, 3.5, 1.4, 0.2},
		}
		
		bodyBytes, _ := json.Marshal(reqBody)
		req, _ := http.NewRequest("POST", "/predict", bytes.NewBuffer(bodyBytes))
		req.Header.Set("Content-Type", "application/json")
		resp := httptest.NewRecorder()
		
		start := time.Now()
		router.ServeHTTP(resp, req)
		latencies[i] = time.Since(start)
	}
	
	// Calculate statistics
	var totalLatency time.Duration
	for _, latency := range latencies {
		totalLatency += latency
	}
	avgLatency := totalLatency / time.Duration(numRequests)
	
	// Assert reasonable performance
	assert.Less(t, avgLatency, 10*time.Millisecond, "Average latency should be less than 10ms")
	
	t.Logf("Average latency: %v", avgLatency)
}
