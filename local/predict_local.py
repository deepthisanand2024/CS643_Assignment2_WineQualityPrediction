#!/usr/bin/env python3
import os
import sys
import boto3
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score

if len(sys.argv) != 3:
    print("Usage: predict_local.py <s3_model_path> <s3_validation_csv>")
    sys.exit(1)

s3_model_path = sys.argv[1]
s3_validation_csv = sys.argv[2]

# Extract bucket and keys
def parse_s3_path(s3_path):
    if not s3_path.startswith("s3://"):
        raise ValueError("Invalid S3 path")
    parts = s3_path.replace("s3://", "").split("/", 1)
    return parts[0], parts[1]

bucket_model, key_model = parse_s3_path(s3_model_path)
bucket_val, key_val = parse_s3_path(s3_validation_csv)

s3 = boto3.client('s3')
local_model = "/tmp/model.joblib"
local_csv = "/tmp/validation.csv"

print(f"📥 Downloading model from {s3_model_path}")
s3.download_file(bucket_model, key_model, local_model)

print(f"📥 Downloading validation dataset from {s3_validation_csv}")
s3.download_file(bucket_val, key_val, local_csv)

print("💾 Loading model")
model = joblib.load(local_model)

print("📂 Reading validation data")
df = pd.read_csv(local_csv, sep=";")
df = df.dropna()

if "quality" not in df.columns:
    raise ValueError("Target column 'quality' missing in validation dataset")

X = df.drop("quality", axis=1)
y = df["quality"]

print("🤖 Running predictions")
preds = model.predict(X)

acc = accuracy_score(y, preds)
print(f"🎯 Prediction Accuracy: {acc:.4f}")

# Save predictions
output_csv = "/tmp/predictions.csv"
df["predicted_quality"] = preds
df.to_csv(output_csv, index=False)
print(f"✅ Predictions saved at {output_csv}")
