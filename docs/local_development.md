# Local Development Guide

## 🔧 Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Run Locally

```bash
python local/predict_local.py \
  s3://wine-quality-bucket-deepthi/wine_model_debug/wine_model_v9.joblib \
  s3://wine-quality-bucket-deepthi/ValidationDataset-1.csv
```

## 🔍 VS Code Debug Configuration

```json
{
    "name": "Local Prediction",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/local/predict_local.py",
    "args": [
        "s3://wine-quality-bucket-deepthi/wine_model_debug/wine_model_v9.joblib",
        "s3://wine-quality-bucket-deepthi/ValidationDataset-1.csv"
    ],
    "console": "integratedTerminal"
}
```

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Run specific test
python -m unittest tests.test_prediction
```

## 📊 Data Analysis

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load and analyze data
df = pd.read_csv('data/ValidationDataset-1.csv')
print(df.describe())

# Plot quality distribution
df['quality'].value_counts().plot(kind='bar')
plt.title('Wine Quality Distribution')
plt.show()
```

## 🔧 Development Workflow

1. **Code changes** → Test locally
2. **Local testing** → Test with Docker  
3. **Docker testing** → Deploy to AWS
4. **AWS testing** → Production ready