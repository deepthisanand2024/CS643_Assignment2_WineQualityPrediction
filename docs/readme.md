# Wine Quality Prediction Project

A machine learning pipeline for predicting wine quality using Docker containers and AWS S3.

## 🎯 Overview

This project downloads trained models and datasets from AWS S3, runs predictions using scikit-learn, and supports multiple deployment environments.

## 🏗️ Architecture

```
AWS S3 → Docker/Local/EMR → Predictions (CSV + Console)
```

## 🚀 Quick Start

```bash
# Build Docker image
./scripts/build_docker.sh

# Run prediction
./scripts/run_docker.sh
```

## 📊 Results

- **Input**: 160 wine samples
- **Output**: Quality predictions (3-9 scale)
- **Format**: CSV file + console output

## 📖 Documentation

- [Docker Guide](docker_guide.md) - Container implementation
- [AWS Setup](aws_setup.md) - Credential configuration  
- [EMR Guide](emr_guide.md) - Spark implementation
- [Local Development](local_development.md) - Local setup
- [Troubleshooting](troubleshooting.md) - Common issues

## 🔧 Requirements

- Python 3.9+
- Docker
- AWS CLI configured
- S3 bucket access

## 📄 License

MIT License