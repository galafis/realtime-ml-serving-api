"""
Model Evaluator for ML Serving API

Evaluate model performance, drift detection, and quality metrics.

Author: Gabriel Demetrios Lafis
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import joblib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns


class ModelEvaluator:
    """
    Comprehensive model evaluation toolkit.
    """
    
    def __init__(self, model_path: str, metadata_path: Optional[str] = None):
        """
        Initialize model evaluator.
        
        Parameters
        ----------
        model_path : str
            Path to the trained model
        metadata_path : str, optional
            Path to model metadata
        """
        self.model = joblib.load(model_path)
        self.model_name = Path(model_path).stem
        
        if metadata_path and Path(metadata_path).exists():
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
    
    def evaluate(
        self,
        X_test: np.ndarray,
        y_test: np.ndarray,
        save_report: bool = True
    ) -> Dict:
        """
        Comprehensive model evaluation.
        
        Parameters
        ----------
        X_test : array-like
            Test features
        y_test : array-like
            Test labels
        save_report : bool
            Whether to save evaluation report
            
        Returns
        -------
        metrics : dict
            Evaluation metrics
        """
        # Make predictions
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
            'recall': float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
            'f1_score': float(f1_score(y_test, y_pred, average='weighted', zero_division=0)),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'n_samples': len(y_test),
            'timestamp': datetime.now().isoformat()
        }
        
        # Add probabilities if available
        if hasattr(self.model, 'predict_proba'):
            y_proba = self.model.predict_proba(X_test)
            
            # For binary classification
            if y_proba.shape[1] == 2:
                try:
                    metrics['roc_auc'] = float(roc_auc_score(y_test, y_proba[:, 1]))
                except:
                    pass
        
        # Detailed classification report
        report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        metrics['classification_report'] = report
        
        # Save report
        if save_report:
            self._save_evaluation_report(metrics)
        
        return metrics
    
    def detect_drift(
        self,
        X_baseline: np.ndarray,
        X_current: np.ndarray,
        threshold: float = 0.1
    ) -> Dict:
        """
        Detect data drift between baseline and current data.
        
        Parameters
        ----------
        X_baseline : array-like
            Baseline feature data
        X_current : array-like
            Current feature data
        threshold : float
            Drift threshold
            
        Returns
        -------
        drift_report : dict
            Drift detection results
        """
        drift_report = {
            'timestamp': datetime.now().isoformat(),
            'features_drift': {},
            'overall_drift': False
        }
        
        n_features = X_baseline.shape[1]
        drifted_features = 0
        
        for i in range(n_features):
            baseline_mean = np.mean(X_baseline[:, i])
            current_mean = np.mean(X_current[:, i])
            baseline_std = np.std(X_baseline[:, i])
            
            # Calculate normalized drift
            if baseline_std > 0:
                drift = abs(current_mean - baseline_mean) / baseline_std
            else:
                drift = 0
            
            feature_drifted = drift > threshold
            if feature_drifted:
                drifted_features += 1
            
            drift_report['features_drift'][f'feature_{i}'] = {
                'drift_score': float(drift),
                'drifted': feature_drifted,
                'baseline_mean': float(baseline_mean),
                'current_mean': float(current_mean),
                'baseline_std': float(baseline_std)
            }
        
        # Overall drift if more than 20% features drifted
        drift_report['overall_drift'] = (drifted_features / n_features) > 0.2
        drift_report['drift_percentage'] = float(drifted_features / n_features)
        
        return drift_report
    
    def compare_models(
        self,
        other_model_path: str,
        X_test: np.ndarray,
        y_test: np.ndarray
    ) -> Dict:
        """
        Compare current model with another model.
        
        Parameters
        ----------
        other_model_path : str
            Path to comparison model
        X_test : array-like
            Test features
        y_test : array-like
            Test labels
            
        Returns
        -------
        comparison : dict
            Model comparison results
        """
        other_model = joblib.load(other_model_path)
        
        # Evaluate both models
        y_pred_current = self.model.predict(X_test)
        y_pred_other = other_model.predict(X_test)
        
        comparison = {
            'current_model': {
                'name': self.model_name,
                'accuracy': float(accuracy_score(y_test, y_pred_current)),
                'f1_score': float(f1_score(y_test, y_pred_current, average='weighted', zero_division=0))
            },
            'other_model': {
                'name': Path(other_model_path).stem,
                'accuracy': float(accuracy_score(y_test, y_pred_other)),
                'f1_score': float(f1_score(y_test, y_pred_other, average='weighted', zero_division=0))
            }
        }
        
        # Determine winner
        if comparison['current_model']['f1_score'] > comparison['other_model']['f1_score']:
            comparison['winner'] = 'current_model'
        elif comparison['current_model']['f1_score'] < comparison['other_model']['f1_score']:
            comparison['winner'] = 'other_model'
        else:
            comparison['winner'] = 'tie'
        
        return comparison
    
    def _save_evaluation_report(self, metrics: Dict):
        """Save evaluation report to file."""
        report_dir = Path('models/evaluations')
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = report_dir / f'{self.model_name}_evaluation_{timestamp}.json'
        
        with open(report_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"Evaluation report saved to: {report_file}")
    
    def plot_confusion_matrix(self, X_test: np.ndarray, y_test: np.ndarray, save_path: Optional[str] = None):
        """Plot confusion matrix."""
        y_pred = self.model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Confusion Matrix - {self.model_name}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Confusion matrix saved to: {save_path}")
        else:
            plt.show()
        
        plt.close()


def main():
    """
    Example usage of ModelEvaluator.
    """
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    
    print("=" * 60)
    print("Model Evaluation Example")
    print("=" * 60)
    
    # Load test data
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Evaluate iris classifier
    try:
        evaluator = ModelEvaluator(
            model_path='models/iris_classifier.pkl',
            metadata_path='models/iris_classifier_metadata.json'
        )
        
        print("\n1. Model Evaluation:")
        metrics = evaluator.evaluate(X_test, y_test)
        print(f"   Accuracy: {metrics['accuracy']:.4f}")
        print(f"   F1 Score: {metrics['f1_score']:.4f}")
        
        print("\n2. Drift Detection:")
        drift_report = evaluator.detect_drift(X_train, X_test)
        print(f"   Overall Drift: {drift_report['overall_drift']}")
        print(f"   Drift Percentage: {drift_report['drift_percentage']:.2%}")
        
        print("\n✓ Evaluation completed successfully!")
        
    except FileNotFoundError:
        print("\n⚠ Model file not found. Please train a model first using train_model.py")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
