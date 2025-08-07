FROM python:3.9-slim

RUN pip install --no-cache-dir boto3 pandas numpy scikit-learn joblib

WORKDIR /app

COPY predict_local_docker.py /app/predict_local_docker.py

ENTRYPOINT ["python", "predict_local_docker.py"]
