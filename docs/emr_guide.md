# EMR/Spark Guide

## 🚀 Create EMR Cluster

```bash
aws emr create-cluster \
  --name "Wine-Quality-Cluster" \
  --release-label emr-6.4.0 \
  --instance-type m5.xlarge \
  --instance-count 3 \
  --applications Name=Spark Name=Hadoop \
  --service-role EMR_DefaultRole \
  --ec2-attributes InstanceProfile=EMR_EC2_DefaultRole
```

## 🎯 Submit Training Job

```bash
spark-submit \
  emr/train_emr_debug_modelsave_v9.py \
  s3://wine-quality-bucket-deepthi/TrainingDataset-1.csv \
  s3://wine-quality-bucket-deepthi/wine_model_debug/wine_model_v9.joblib
```

## 🔮 Submit Prediction Job

```bash
spark-submit \
  emr/predict_emr.py \
  s3://wine-quality-bucket-deepthi/ValidationDataset-1.csv \
  s3://wine-quality-bucket-deepthi/wine_model_debug/
```

## 📊 Local Spark Testing

```bash
# Install PySpark
pip install pyspark

# Test locally
python emr/train_emr_debug_modelsave_v9.py \
  data/TrainingDataset-1.csv \
  s3://bucket/model.joblib
```

## 🔍 Monitoring

- **Spark UI**: http://master-public-dns:20888/
- **Logs**: Check EMR step logs in CloudWatch
- **Status**: `aws emr describe-cluster --cluster-id j-XXXXXXXXX`

## 💰 Cost Optimization

```bash
# Use spot instances
aws emr create-cluster \
  --instance-groups \
    InstanceGroupType=MASTER,InstanceType=m5.xlarge,InstanceCount=1 \
    InstanceGroupType=CORE,InstanceType=m5.xlarge,InstanceCount=2,BidPrice=0.10

# Auto-terminate
aws emr create-cluster --auto-terminate
```