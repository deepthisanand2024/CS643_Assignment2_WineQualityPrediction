# AWS Setup Guide

## 🔧 Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## 🔑 Configure Credentials

### Method 1: AWS CLI
```bash
aws configure
# Enter: Access Key, Secret Key, Region (us-east-1), Format (json)
```

### Method 2: Environment Variables
```bash
export AWS_ACCESS_KEY_ID="your_key"
export AWS_SECRET_ACCESS_KEY="your_secret"
export AWS_DEFAULT_REGION="us-east-1"
```

### Method 3: CloudShell
Automatic - no configuration needed

## 🛡️ Required Permissions

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::wine-quality-bucket-deepthi",
                "arn:aws:s3:::wine-quality-bucket-deepthi/*"
            ]
        }
    ]
}
```

## 🔍 Test Access

```bash
# Check credentials
aws sts get-caller-identity

# Test S3 access
aws s3 ls s3://wine-quality-bucket-deepthi/

# Test specific file
aws s3 ls s3://wine-quality-bucket-deepthi/wine_model_debug/wine_model_v9.joblib
```

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| NoCredentialsError | Run `aws configure` or set environment variables |
| AccessDenied | Check IAM permissions |
| Invalid endpoint | Set `AWS_DEFAULT_REGION=us-east-1` |
| File not found | Verify S3 paths with `aws s3 ls` |