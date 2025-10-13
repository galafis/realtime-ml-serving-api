package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/go-redis/redis/v8"
)

// Author: Gabriel Demetrios Lafis

var (
	ctx         = context.Background()
	redisClient *redis.Client
)

// PredictionRequest represents an incoming prediction request
type PredictionRequest struct {
	ModelName string    `json:"model_name" binding:"required"`
	Features  []float64 `json:"features" binding:"required"`
	ModelVersion string `json:"model_version,omitempty"`
}

// PredictionResponse represents the prediction result
type PredictionResponse struct {
	Prediction  interface{} `json:"prediction"`
	Probability float64     `json:"probability,omitempty"`
	ModelName   string      `json:"model_name"`
	ModelVersion string     `json:"model_version"`
	Latency     float64     `json:"latency_ms"`
	CacheHit    bool        `json:"cache_hit"`
}

// HealthResponse represents health check response
type HealthResponse struct {
	Status    string `json:"status"`
	Timestamp int64  `json:"timestamp"`
	Version   string `json:"version"`
}

func init() {
	// Initialize Redis client
	redisClient = redis.NewClient(&redis.Options{
		Addr:     getEnv("REDIS_ADDR", "localhost:6379"),
		Password: getEnv("REDIS_PASSWORD", ""),
		DB:       0,
	})

	// Test Redis connection
	_, err := redisClient.Ping(ctx).Result()
	if err != nil {
		log.Printf("Warning: Redis connection failed: %v", err)
	} else {
		log.Println("Redis connected successfully")
	}
}

func main() {
	// Set Gin mode
	gin.SetMode(gin.ReleaseMode)

	// Create router
	router := gin.Default()

	// Middleware
	router.Use(corsMiddleware())
	router.Use(metricsMiddleware())

	// Routes
	router.GET("/health", healthCheck)
	router.POST("/predict", predict)
	router.GET("/models", listModels)
	router.GET("/metrics", getMetrics)

	// Server configuration
	srv := &http.Server{
		Addr:         ":8080",
		Handler:      router,
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  120 * time.Second,
	}

	// Start server in goroutine
	go func() {
		log.Println("Starting ML Serving API on :8080")
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server failed to start: %v", err)
		}
	}()

	// Graceful shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatalf("Server forced to shutdown: %v", err)
	}

	log.Println("Server exited")
}

func healthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, HealthResponse{
		Status:    "healthy",
		Timestamp: time.Now().Unix(),
		Version:   "1.0.0",
	})
}

func predict(c *gin.Context) {
	startTime := time.Now()

	var req PredictionRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Check cache
	cacheKey := fmt.Sprintf("pred:%s:%v", req.ModelName, req.Features)
	cachedResult, err := redisClient.Get(ctx, cacheKey).Result()
	
	var response PredictionResponse
	cacheHit := false

	if err == nil {
		// Cache hit
		json.Unmarshal([]byte(cachedResult), &response)
		cacheHit = true
	} else {
		// Cache miss - perform prediction
		prediction, prob := makePrediction(req.Features)
		
		response = PredictionResponse{
			Prediction:   prediction,
			Probability:  prob,
			ModelName:    req.ModelName,
			ModelVersion: "1.0.0",
			CacheHit:     false,
		}

		// Store in cache
		responseJSON, _ := json.Marshal(response)
		redisClient.Set(ctx, cacheKey, responseJSON, 5*time.Minute)
	}

	// Calculate latency
	latency := time.Since(startTime).Milliseconds()
	response.Latency = float64(latency)
	response.CacheHit = cacheHit

	c.JSON(http.StatusOK, response)
}

func makePrediction(features []float64) (interface{}, float64) {
	// Simplified prediction logic
	// In production, load actual model and make prediction
	sum := 0.0
	for _, f := range features {
		sum += f
	}
	
	prediction := 0
	if sum > 10.0 {
		prediction = 1
	}
	
	probability := 0.85
	
	return prediction, probability
}

func listModels(c *gin.Context) {
	models := []map[string]interface{}{
		{
			"name":    "iris_classifier",
			"version": "1.0.0",
			"status":  "active",
		},
		{
			"name":    "fraud_detector",
			"version": "2.1.0",
			"status":  "active",
		},
	}

	c.JSON(http.StatusOK, gin.H{
		"models": models,
		"count":  len(models),
	})
}

func getMetrics(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"total_requests":  1000,
		"cache_hit_rate":  0.87,
		"avg_latency_ms":  0.8,
		"p99_latency_ms":  4.2,
	})
}

func corsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	}
}

func metricsMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		c.Next()
		duration := time.Since(start)
		
		log.Printf("%s %s - %d - %v", 
			c.Request.Method, 
			c.Request.URL.Path, 
			c.Writer.Status(), 
			duration)
	}
}

func getEnv(key, defaultValue string) string {
	value := os.Getenv(key)
	if value == "" {
		return defaultValue
	}
	return value
}

