#!/usr/bin/env python3
import sys
import os
import pandas as pd
import joblib
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
from pyspark.sql import SparkSession
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

LOGFILE = "/mnt/var/log/hadoop/steps/train_emr_debug_modelsave_v9.log"

def log(msg):
    print(msg)
    with open(LOGFILE, "a") as f:
        f.write(msg + "\n")

if len(sys.argv) != 3:
    log("❌ Usage: train_emr_debug_modelsave_v9.py <s3_input_csv> <s3_model_path>")
    sys.exit(1)

input_csv = sys.argv[1]
s3_model_path = sys.argv[2]
local_model_path = "/tmp/wine_model_v9.joblib"

log("🚀 Starting Spark Session")
spark = SparkSession.builder.appName("WineQualityTraining_v9").getOrCreate()

try:
    # ====== Load Dataset ======
    log(f"📥 Reading dataset from {input_csv}")
    df = spark.read.option("header", "true").option("inferSchema", "true").option("delimiter", ";").csv(input_csv)
    df = df.na.drop()

    # Clean column names (remove quotes, spaces)
    df = df.toDF(*[c.replace('"', '').replace("'", '').strip().lower() for c in df.columns])
    log(f"✅ Cleaned Columns: {df.columns}")

    # Ensure target column exists
    if "quality" not in df.columns:
        raise ValueError(f"❌ Target column 'quality' not found in {df.columns}")

    pdf = df.toPandas()
    X = pdf.drop("quality", axis=1)
    y = pdf["quality"]

    # ====== Train Model ======
    log("🤖 Training RandomForest model")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    log(f"🎯 Model trained successfully with accuracy: {acc:.4f}")

    # ====== Save Locally ======
    joblib.dump(model, local_model_path)
    log(f"💾 Model saved locally at {local_model_path}")

    # ====== Upload to S3 using boto3 ======
    log(f"☁️ Uploading model to {s3_model_path} using boto3")
    try:
        s3 = boto3.client('s3')
        bucket_name = s3_model_path.split('/')[2]
        key = '/'.join(s3_model_path.split('/')[3:])
        s3.upload_file(local_model_path, bucket_name, key)
        log("✅ Model uploaded successfully to S3")
    except (BotoCoreError, NoCredentialsError) as e:
        log(f"❌ Boto3 S3 upload failed: {str(e)}")
        sys.exit(1)

    log("🏁 Training completed successfully!")

except Exception as e:
    log(f"❌ Exception: {str(e)}")
    sys.exit(1)
finally:
    spark.stop()
