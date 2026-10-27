import os

import boto3
from dotenv import load_dotenv
from botocore.exceptions import BotoCoreError, ClientError

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3_client = boto3.client("s3", region_name=AWS_REGION)

def check_bucket_access():
    """Check whether the configured s3 bucket is accessible"""
    if not S3_BUCKET_NAME:
        raise ValueError("S3_BUCKET_NAME is missing from .env")

    try:
        s3_client.head_bucket(Bucket=S3_BUCKET_NAME)
        print(f"S3 bucket access successful: {S3_BUCKET_NAME}")
        return True

    except {BotoCoreError, ClientError} as error:
        print(f"S3 bucket access failed: {error}")
        return False

def upload_document(file_path: str, object_key: str):
    """Upload a local document to the project's S3 prefix."""
    if not S3_BUCKET_NAME:
        raise ValueError("S3_BUCKET_NAME is missing from .env")

    if not object_key.startswith("document-qa/uploads/"):
        raise ValueError(f"Object key must use the document-qa/uploads prefix")

    try:
        s3_client.upload_file(file_path, S3_BUCKET_NAME, object_key)

        print(f"Upload successful: s3://{S3_BUCKET_NAME}/{object_key}")
        return True

    except {BotoCoreError, ClientError} as error:
        print(f"S3 upload failed: {error}")
        return False