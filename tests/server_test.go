package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

// Author: Gabriel Demetrios Lafis

func TestHealthCheck(t *testing.T) {
	gin.SetMode(gin.TestMode)
	
	router := gin.Default()
	router.GET("/health", healthCheck)
	
	req, _ := http.NewRequest("GET", "/health", nil)
	resp := httptest.NewRecorder()
	
	router.ServeHTTP(resp, req)
	
	assert.Equal(t, http.StatusOK, resp.Code)
	
	var response HealthResponse
	err := json.Unmarshal(resp.Body.Bytes(), &response)
	assert.NoError(t, err)
	assert.Equal(t, "healthy", response.Status)
	assert.Equal(t, "1.0.0", response.Version)
}

func TestPredictEndpoint(t *testing.T) {
	gin.SetMode(gin.TestMode)
	
	router := gin.Default()
	router.POST("/predict", predict)
	
	// Test valid request
	t.Run("Valid prediction request", func(t *testing.T) {
		requestBody := `{
			"model_name": "iris_classifier",
			"features": [5.1, 3.5, 1.4, 0.2]
		}`
		
		req, _ := http.NewRequest("POST", "/predict", strings.NewReader(requestBody))
		req.Header.Set("Content-Type", "application/json")
		resp := httptest.NewRecorder()
		
		router.ServeHTTP(resp, req)
		
		assert.Equal(t, http.StatusOK, resp.Code)
		
		var response PredictionResponse
		err := json.Unmarshal(resp.Body.Bytes(), &response)
		assert.NoError(t, err)
		assert.Equal(t, "iris_classifier", response.ModelName)
		assert.NotNil(t, response.Prediction)
	})
	
	// Test invalid request (missing fields)
	t.Run("Invalid prediction request", func(t *testing.T) {
		requestBody := `{
			"model_name": "iris_classifier"
		}`
		
		req, _ := http.NewRequest("POST", "/predict", strings.NewReader(requestBody))
		req.Header.Set("Content-Type", "application/json")
		resp := httptest.NewRecorder()
		
		router.ServeHTTP(resp, req)
		
		assert.Equal(t, http.StatusBadRequest, resp.Code)
	})
}

func TestListModels(t *testing.T) {
	gin.SetMode(gin.TestMode)
	
	router := gin.Default()
	router.GET("/models", listModels)
	
	req, _ := http.NewRequest("GET", "/models", nil)
	resp := httptest.NewRecorder()
	
	router.ServeHTTP(resp, req)
	
	assert.Equal(t, http.StatusOK, resp.Code)
	
	var response map[string]interface{}
	err := json.Unmarshal(resp.Body.Bytes(), &response)
	assert.NoError(t, err)
	
	assert.Contains(t, response, "models")
	assert.Contains(t, response, "count")
	
	models := response["models"].([]interface{})
	assert.Greater(t, len(models), 0)
}

func TestGetMetrics(t *testing.T) {
	gin.SetMode(gin.TestMode)
	
	router := gin.Default()
	router.GET("/metrics", getMetrics)
	
	req, _ := http.NewRequest("GET", "/metrics", nil)
	resp := httptest.NewRecorder()
	
	router.ServeHTTP(resp, req)
	
	assert.Equal(t, http.StatusOK, resp.Code)
	
	var response map[string]interface{}
	err := json.Unmarshal(resp.Body.Bytes(), &response)
	assert.NoError(t, err)
	
	assert.Contains(t, response, "total_requests")
	assert.Contains(t, response, "cache_hit_rate")
	assert.Contains(t, response, "avg_latency_ms")
	assert.Contains(t, response, "p99_latency_ms")
}

func TestCORSMiddleware(t *testing.T) {
	gin.SetMode(gin.TestMode)
	
	router := gin.Default()
	router.Use(corsMiddleware())
	router.GET("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"message": "test"})
	})
	
	req, _ := http.NewRequest("GET", "/test", nil)
	resp := httptest.NewRecorder()
	
	router.ServeHTTP(resp, req)
	
	assert.Equal(t, "*", resp.Header().Get("Access-Control-Allow-Origin"))
	assert.Contains(t, resp.Header().Get("Access-Control-Allow-Methods"), "GET")
}

func TestMakePrediction(t *testing.T) {
	// Test prediction logic
	t.Run("Sum less than 10", func(t *testing.T) {
		features := []float64{1.0, 2.0, 3.0}
		prediction, probability := makePrediction(features)
		
		assert.Equal(t, 0, prediction)
		assert.Equal(t, 0.85, probability)
	})
	
	t.Run("Sum greater than 10", func(t *testing.T) {
		features := []float64{5.0, 5.0, 5.0}
		prediction, probability := makePrediction(features)
		
		assert.Equal(t, 1, prediction)
		assert.Equal(t, 0.85, probability)
	})
}
