import sys
import os
import boto3
import joblib
import pandas as pd
from io import BytesIO

def s3_to_local(s3_uri, local_path):
    s3 = boto3.client('s3')
    bucket, key = s3_uri.replace("s3://", "").split("/", 1)
    print(f"📥 Downloading {s3_uri} -> {local_path}")
    s3.download_file(bucket, key, local_path)
    print(f"✅ Successfully downloaded to {local_path}")

def load_model(path):
    print("🤖 Loading model...")
    return joblib.load(path)

def load_data(path):
    print("📊 Loading data...")
    df = pd.read_csv(path)
    return df

def predict(model, data):
    print("🔮 Making predictions...")
    return model.predict(data)

def save_predictions(predictions, path="/tmp/predictions.csv"):
    df = pd.DataFrame(predictions, columns=["prediction"])
    df.to_csv(path, index=False)
    print(f"💾 Predictions saved to {path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python predict_local_docker.py <model_s3_uri> <data_s3_uri>")
        sys.exit(1)

    model_s3 = sys.argv[1]
    data_s3 = sys.argv[2]
    local_model = "/tmp/model.joblib"
    local_data = "/tmp/input.csv"

    print(f"✅ AWS credentials found for account: {boto3.client('sts').get_caller_identity().get('Account')}")

    s3_to_local(model_s3, local_model)
    s3_to_local(data_s3, local_data)

    try:
        model = load_model(local_model)
        data = load_data(local_data)

        if 'target' in data.columns:
            data = data.drop(columns=['target'])

        predictions = predict(model, data)
        print(f"✅ Predictions complete. Shape: {predictions.shape}")
        print(f"First 10 predictions: {predictions[:10]}")
        save_predictions(predictions)
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
