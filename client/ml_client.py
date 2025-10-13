"""
Python client for Real-Time ML Serving API

Author: Gabriel Demetrios Lafis
"""

import requests
import numpy as np
from typing import Dict, List, Optional
import time


class MLClient:
    """
    Client for interacting with the ML Serving API.
    """
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        """
        Initialize ML client.
        
        Parameters
        ----------
        base_url : str
            Base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
    def predict(
        self,
        model_name: str,
        features: List[float],
        model_version: Optional[str] = None
    ) -> Dict:
        """
        Make a prediction.
        
        Parameters
        ----------
        model_name : str
            Name of the model
        features : list
            Feature values
        model_version : str, optional
            Specific model version
            
        Returns
        -------
        result : dict
            Prediction result
        """
        url = f"{self.base_url}/predict"
        
        payload = {
            "model_name": model_name,
            "features": features
        }
        
        if model_version:
            payload["model_version"] = model_version
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def batch_predict(
        self,
        model_name: str,
        features_list: List[List[float]]
    ) -> List[Dict]:
        """
        Make batch predictions.
        
        Parameters
        ----------
        model_name : str
            Name of the model
        features_list : list of lists
            List of feature vectors
            
        Returns
        -------
        results : list
            List of prediction results
        """
        results = []
        
        for features in features_list:
            result = self.predict(model_name, features)
            results.append(result)
        
        return results
    
    def list_models(self) -> Dict:
        """
        List available models.
        
        Returns
        -------
        models : dict
            Available models
        """
        url = f"{self.base_url}/models"
        response = self.session.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def get_metrics(self) -> Dict:
        """
        Get API metrics.
        
        Returns
        -------
        metrics : dict
            API metrics
        """
        url = f"{self.base_url}/metrics"
        response = self.session.get(url)
        response.raise_for_status()
        
        return response.json()
    
    def health_check(self) -> bool:
        """
        Check API health.
        
        Returns
        -------
        is_healthy : bool
            Whether API is healthy
        """
        try:
            url = f"{self.base_url}/health"
            response = self.session.get(url, timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def benchmark(
        self,
        model_name: str,
        features: List[float],
        n_requests: int = 1000
    ) -> Dict:
        """
        Benchmark API performance.
        
        Parameters
        ----------
        model_name : str
            Model to benchmark
        features : list
            Sample features
        n_requests : int
            Number of requests to make
            
        Returns
        -------
        stats : dict
            Performance statistics
        """
        latencies = []
        
        for _ in range(n_requests):
            start = time.time()
            self.predict(model_name, features)
            latency = (time.time() - start) * 1000  # ms
            latencies.append(latency)
        
        latencies = np.array(latencies)
        
        return {
            'mean_latency_ms': np.mean(latencies),
            'median_latency_ms': np.median(latencies),
            'p95_latency_ms': np.percentile(latencies, 95),
            'p99_latency_ms': np.percentile(latencies, 99),
            'min_latency_ms': np.min(latencies),
            'max_latency_ms': np.max(latencies),
            'total_requests': n_requests,
            'throughput_rps': n_requests / (np.sum(latencies) / 1000)
        }


if __name__ == "__main__":
    # Example usage
    client = MLClient()
    
    # Check health
    if client.health_check():
        print("✓ API is healthy")
    
    # List models
    models = client.list_models()
    print(f"\nAvailable models: {models['count']}")
    
    # Make prediction
    result = client.predict(
        model_name="iris_classifier",
        features=[5.1, 3.5, 1.4, 0.2]
    )
    print(f"\nPrediction: {result['prediction']}")
    print(f"Latency: {result['latency_ms']}ms")
    print(f"Cache hit: {result['cache_hit']}")
    
    # Benchmark
    print("\nRunning benchmark...")
    stats = client.benchmark(
        model_name="iris_classifier",
        features=[5.1, 3.5, 1.4, 0.2],
        n_requests=100
    )
    print(f"Mean latency: {stats['mean_latency_ms']:.2f}ms")
    print(f"P99 latency: {stats['p99_latency_ms']:.2f}ms")
    print(f"Throughput: {stats['throughput_rps']:.0f} req/s")

