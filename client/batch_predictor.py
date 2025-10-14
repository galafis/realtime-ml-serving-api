"""
Batch Predictor for ML Serving API

Efficient batch prediction processing with parallel execution.

Author: Gabriel Demetrios Lafis
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Union
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from ml_client import MLClient
import json
from pathlib import Path
from datetime import datetime


class BatchPredictor:
    """
    High-performance batch prediction client.
    """
    
    def __init__(
        self,
        base_url: str = "http://localhost:8080",
        max_workers: int = 10
    ):
        """
        Initialize batch predictor.
        
        Parameters
        ----------
        base_url : str
            Base URL of the ML serving API
        max_workers : int
            Maximum number of parallel workers
        """
        self.client = MLClient(base_url)
        self.max_workers = max_workers
    
    def predict_batch(
        self,
        model_name: str,
        features_list: List[List[float]],
        parallel: bool = True
    ) -> List[Dict]:
        """
        Make batch predictions.
        
        Parameters
        ----------
        model_name : str
            Name of the model to use
        features_list : list of lists
            List of feature vectors
        parallel : bool
            Whether to use parallel execution
            
        Returns
        -------
        results : list
            List of prediction results
        """
        if parallel and len(features_list) > 10:
            return self._predict_parallel(model_name, features_list)
        else:
            return self._predict_sequential(model_name, features_list)
    
    def _predict_sequential(
        self,
        model_name: str,
        features_list: List[List[float]]
    ) -> List[Dict]:
        """Sequential batch prediction."""
        results = []
        
        for i, features in enumerate(features_list):
            try:
                result = self.client.predict(model_name, features)
                result['batch_index'] = i
                results.append(result)
            except Exception as e:
                results.append({
                    'batch_index': i,
                    'error': str(e),
                    'prediction': None
                })
        
        return results
    
    def _predict_parallel(
        self,
        model_name: str,
        features_list: List[List[float]]
    ) -> List[Dict]:
        """Parallel batch prediction using ThreadPoolExecutor."""
        results = [None] * len(features_list)
        
        def predict_single(index: int, features: List[float]) -> Dict:
            try:
                result = self.client.predict(model_name, features)
                result['batch_index'] = index
                return index, result
            except Exception as e:
                return index, {
                    'batch_index': index,
                    'error': str(e),
                    'prediction': None
                }
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(predict_single, i, features): i
                for i, features in enumerate(features_list)
            }
            
            for future in as_completed(futures):
                index, result = future.result()
                results[index] = result
        
        return results
    
    def predict_from_csv(
        self,
        model_name: str,
        csv_path: str,
        feature_columns: Optional[List[str]] = None,
        output_path: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Make predictions from CSV file.
        
        Parameters
        ----------
        model_name : str
            Name of the model
        csv_path : str
            Path to input CSV file
        feature_columns : list, optional
            List of feature column names. If None, use all columns
        output_path : str, optional
            Path to save output CSV
            
        Returns
        -------
        df_results : DataFrame
            Results with predictions
        """
        # Load CSV
        df = pd.read_csv(csv_path)
        
        # Extract features
        if feature_columns:
            features_list = df[feature_columns].values.tolist()
        else:
            features_list = df.values.tolist()
        
        # Make predictions
        print(f"Making predictions for {len(features_list)} samples...")
        start_time = time.time()
        
        results = self.predict_batch(model_name, features_list, parallel=True)
        
        elapsed_time = time.time() - start_time
        print(f"Completed in {elapsed_time:.2f}s ({len(features_list)/elapsed_time:.0f} predictions/sec)")
        
        # Add predictions to dataframe
        df['prediction'] = [r.get('prediction') for r in results]
        df['probability'] = [r.get('probability') for r in results]
        df['latency_ms'] = [r.get('latency_ms') for r in results]
        df['cache_hit'] = [r.get('cache_hit', False) for r in results]
        
        # Save output
        if output_path:
            df.to_csv(output_path, index=False)
            print(f"Results saved to: {output_path}")
        
        return df
    
    def predict_streaming(
        self,
        model_name: str,
        features_generator,
        batch_size: int = 100,
        callback=None
    ):
        """
        Stream predictions in batches.
        
        Parameters
        ----------
        model_name : str
            Name of the model
        features_generator : generator
            Generator yielding feature vectors
        batch_size : int
            Batch size for processing
        callback : callable, optional
            Callback function for each batch result
        """
        batch = []
        batch_count = 0
        total_predictions = 0
        
        for features in features_generator:
            batch.append(features)
            
            if len(batch) >= batch_size:
                # Process batch
                results = self.predict_batch(model_name, batch, parallel=True)
                
                if callback:
                    callback(results)
                
                total_predictions += len(batch)
                batch_count += 1
                print(f"Processed batch {batch_count}: {total_predictions} predictions")
                
                batch = []
        
        # Process remaining
        if batch:
            results = self.predict_batch(model_name, batch, parallel=True)
            if callback:
                callback(results)
            total_predictions += len(batch)
            print(f"Processed final batch: {total_predictions} total predictions")
    
    def benchmark_batch(
        self,
        model_name: str,
        features: List[float],
        batch_sizes: List[int] = [1, 10, 50, 100, 500, 1000]
    ) -> Dict:
        """
        Benchmark different batch sizes.
        
        Parameters
        ----------
        model_name : str
            Name of the model
        features : list
            Sample feature vector
        batch_sizes : list
            List of batch sizes to test
            
        Returns
        -------
        benchmark_results : dict
            Benchmark results
        """
        results = {}
        
        for batch_size in batch_sizes:
            print(f"\nTesting batch size: {batch_size}")
            
            # Create batch
            features_list = [features] * batch_size
            
            # Time the prediction
            start_time = time.time()
            predictions = self.predict_batch(model_name, features_list, parallel=True)
            elapsed_time = time.time() - start_time
            
            # Calculate metrics
            throughput = batch_size / elapsed_time
            avg_latency = (elapsed_time / batch_size) * 1000  # ms
            
            results[batch_size] = {
                'total_time': elapsed_time,
                'throughput': throughput,
                'avg_latency_ms': avg_latency,
                'successful': sum(1 for p in predictions if p.get('prediction') is not None)
            }
            
            print(f"  Throughput: {throughput:.0f} req/s")
            print(f"  Avg latency: {avg_latency:.2f}ms")
        
        return results


def main():
    """
    Example usage of BatchPredictor.
    """
    print("=" * 60)
    print("Batch Prediction Example")
    print("=" * 60)
    
    predictor = BatchPredictor(base_url="http://localhost:8080", max_workers=10)
    
    # Check if API is available
    if not predictor.client.health_check():
        print("\n⚠ API is not available. Please start the server first.")
        print("  Run: cd server && ./ml-server")
        return
    
    print("\n✓ API is healthy")
    
    # Example 1: Simple batch prediction
    print("\n1. Simple Batch Prediction:")
    features_list = [
        [5.1, 3.5, 1.4, 0.2],
        [6.2, 2.9, 4.3, 1.3],
        [7.3, 2.9, 6.3, 1.8],
        [5.0, 3.0, 1.6, 0.2],
        [6.3, 3.3, 6.0, 2.5]
    ]
    
    start = time.time()
    results = predictor.predict_batch("iris_classifier", features_list, parallel=True)
    elapsed = time.time() - start
    
    print(f"   Predictions: {[r['prediction'] for r in results]}")
    print(f"   Time: {elapsed:.3f}s")
    print(f"   Throughput: {len(features_list)/elapsed:.0f} req/s")
    
    # Example 2: Benchmark different batch sizes
    print("\n2. Batch Size Benchmark:")
    benchmark_results = predictor.benchmark_batch(
        model_name="iris_classifier",
        features=[5.1, 3.5, 1.4, 0.2],
        batch_sizes=[1, 10, 50, 100]
    )
    
    print("\n" + "=" * 60)
    print("Batch prediction examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
