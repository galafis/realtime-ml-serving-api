# ML Models Directory

This directory contains trained machine learning models used by the API.

## Structure

```
models/
├── iris_classifier.pkl              # Iris species classifier
├── iris_classifier_metadata.json    # Model metadata
├── binary_classifier.pkl            # Binary classifier
├── binary_classifier_metadata.json  # Model metadata
└── metadata/                        # Additional metadata files
```

## Training Models

To train models:

```bash
cd client
python train_model.py
```

## Model Files

Models are saved in pickle format (.pkl) with accompanying metadata in JSON format.

### Metadata Structure

```json
{
  "model_name": "iris_classifier",
  "timestamp": "2024-01-15T10:30:00",
  "metrics": {
    "accuracy": 0.9667,
    "cv_mean": 0.9600,
    "cv_std": 0.0211
  },
  "model_type": "RandomForestClassifier"
}
```

## Adding New Models

1. Train your model using scikit-learn or compatible framework
2. Save the model:
   ```python
   import joblib
   joblib.dump(model, 'models/my_model.pkl')
   ```
3. Create metadata JSON file
4. Add model configuration to `config/models.yaml`
5. Restart the server

## Model Versioning

Models are versioned using:
- Git tags for releases
- Metadata timestamps
- Version field in `models.yaml`

## Best Practices

- Always include metadata with your models
- Test models before deploying to production
- Keep previous versions for rollback
- Document model features and preprocessing steps
- Monitor model performance and drift

## Security

Note: Model files (.pkl) are excluded from git by default in `.gitignore` for security and size reasons. For production, store models in:
- S3 or object storage
- Model registry (MLflow)
- Artifact repository

For development, commit small test models or use Git LFS for larger files.
