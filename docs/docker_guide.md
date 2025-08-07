# Docker Implementation Guide

## 🐳 Build

```bash
docker build --no-cache -t wine-predictor ./docker/
```

## 🚀 Run

### CloudShell (Recommended)
```bash
docker run --rm \
  --network host \
  -e AWS_CONTAINER_CREDENTIALS_FULL_URI \
  -e AWS_CONTAINER_AUTHORIZATION_TOKEN \
  -e AWS_REGION="us-east-1" \
  wine-predictor \
  s3://bucket/model.joblib \
  s3://bucket/data.csv
```

### Standard AWS CLI
```bash
docker run --rm \
  -v ~/.aws:/root/.aws:ro \
  wine-predictor \
  s3://bucket/model.joblib \
  s3://bucket/data.csv
```

### Environment Variables
```bash
docker run --rm \
  -e AWS_ACCESS_KEY_ID="your_key" \
  -e AWS_SECRET_ACCESS_KEY="your_secret" \
  -e AWS_DEFAULT_REGION="us-east-1" \
  wine-predictor \
  s3://bucket/model.joblib \
  s3://bucket/data.csv
```

## 📝 Expected Output

```
✅ AWS credentials found for account: 698381977879
📥 Downloading s3://bucket/model.joblib -> /tmp/model.joblib
✅ Successfully downloaded to /tmp/model.joblib
🤖 Loading model...
🔮 Making predictions...
✅ Predictions complete. Shape: (160,)
First 10 predictions: [5 5 5 5 6 5 5 5 5 5]
💾 Predictions saved to /tmp/predictions.csv
```

## 🔧 Debug

```bash
# Interactive mode
docker run --rm -it --entrypoint bash wine-predictor

# Check logs
docker logs <container_id>
```