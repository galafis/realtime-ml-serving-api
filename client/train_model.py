"""
Model Training Script

Train and save ML models for the serving API.

Author: Gabriel Demetrios Lafis
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, load_iris
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import json
from pathlib import Path
from datetime import datetime


def train_iris_classifier():
    """
    Train a classifier on the Iris dataset.
    
    Returns
    -------
    model : sklearn model
        Trained model
    metrics : dict
        Training metrics
    """
    print("Training Iris Classifier...")
    
    # Load data
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    
    metrics = {
        'accuracy': float(accuracy),
        'cv_mean': float(cv_scores.mean()),
        'cv_std': float(cv_scores.std()),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        'classification_report': classification_report(y_test, y_pred, 
                                                       target_names=iris.target_names,
                                                       output_dict=True)
    }
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    return model, metrics


def train_binary_classifier():
    """
    Train a binary classifier on synthetic data.
    
    Returns
    -------
    model : sklearn model
        Trained model
    metrics : dict
        Training metrics
    """
    print("\nTraining Binary Classifier...")
    
    # Generate synthetic data
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train model
    model = GradientBoostingClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    
    metrics = {
        'accuracy': float(accuracy),
        'cv_mean': float(cv_scores.mean()),
        'cv_std': float(cv_scores.std()),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    return model, metrics


def save_model(model, metrics, model_name: str, models_dir: str = "../models"):
    """
    Save model and metadata.
    
    Parameters
    ----------
    model : sklearn model
        Trained model
    metrics : dict
        Training metrics
    model_name : str
        Name for the model
    models_dir : str
        Directory to save models
    """
    # Create models directory
    models_path = Path(models_dir)
    models_path.mkdir(exist_ok=True)
    
    # Save model
    model_file = models_path / f"{model_name}.pkl"
    joblib.dump(model, model_file)
    print(f"Model saved to: {model_file}")
    
    # Save metadata
    metadata = {
        'model_name': model_name,
        'timestamp': datetime.now().isoformat(),
        'metrics': metrics,
        'model_type': type(model).__name__
    }
    
    metadata_file = models_path / f"{model_name}_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Metadata saved to: {metadata_file}")


def main():
    """
    Main training pipeline.
    """
    print("=" * 60)
    print("ML Model Training Pipeline")
    print("=" * 60)
    
    # Train Iris classifier
    iris_model, iris_metrics = train_iris_classifier()
    save_model(iris_model, iris_metrics, "iris_classifier")
    
    # Train binary classifier
    binary_model, binary_metrics = train_binary_classifier()
    save_model(binary_model, binary_metrics, "binary_classifier")
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print("=" * 60)
    
    # Print summary
    print("\nModel Summary:")
    print(f"  - iris_classifier: {iris_metrics['accuracy']:.4f} accuracy")
    print(f"  - binary_classifier: {binary_metrics['accuracy']:.4f} accuracy")


if __name__ == "__main__":
    main()

