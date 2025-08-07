# Troubleshooting Guide

## 🔐 AWS Credential Issues

### NoCredentialsError
```bash
# Fix: Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
```

### Access Denied
```bash
# Check permissions
aws iam list-attached-user-policies --user-name YOUR_USERNAME

# Test S3 access
aws s3 ls s3://wine-quality-bucket-deepthi/
```

### Invalid Endpoint
```bash
# Set region explicitly
export AWS_DEFAULT_REGION="us-east-1"
```

## 🐳 Docker Issues

### Build Failures
```bash
# Clear cache and rebuild
docker system prune -a
docker build --no-cache -t wine-predictor ./docker/
```

### Container Exits
```bash
# Run interactively to debug
docker run --rm -it --entrypoint bash wine-predictor

# Check logs
docker logs <container_id>
```

### CloudShell Network Issues
```bash
# Always use --network host in CloudShell
docker run --rm --network host wine-predictor
```

## 📁 File Issues

### S3 File Not Found
```bash
# Verify file exists
aws s3 ls s3://wine-quality-bucket-deepthi/wine_model_debug/

# Check exact path
aws s3 ls s3://wine-quality-bucket-deepthi/ --recursive | grep model
```

### Permission Denied
```bash
# Fix file permissions
chmod 644 data/*.csv
chmod 755 scripts/*.sh
```

## 🐍 Python Issues

### Module Not Found
```bash
# Activate virtual environment
source venv/bin/activate

# Install missing packages
pip install -r requirements.txt

# Check installed packages
pip list
```

### Memory Errors
```python
# Process data in chunks
for chunk in pd.read_csv(file, chunksize=1000):
    process_chunk(chunk)

# Clear memory
del large_variable
import gc; gc.collect()
```

## 🔍 Model Issues

### Model Loading Errors
```bash
# Check model file integrity
aws s3 cp s3://bucket/model.joblib ./test_model.joblib
python -c "import joblib; joblib.load('test_model.joblib')"
```

### Prediction Errors
```python
# Check data shape and types
print(f"Data shape: {data.shape}")
print(f"Data dtypes:\n{data.dtypes}")
print(f"Missing values: {data.isnull().sum().sum()}")
```

## 📞 Getting Help

1. Check this troubleshooting guide
2. Verify AWS credentials and permissions
3. Test with minimal examples
4. Check log files for detailed errors
5. Use interactive debugging mode