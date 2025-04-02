import boto3
import os

# Set up credentials
aws_access_key = os.environ['aws_access_key']
aws_secret_key = os.environ['aws_secret_key']
region_name = "ap-south-1"

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
)

bucket_name = 'celeb-images-demo'

# Upload a file
file_path = 'test.txt'
key_name = 'uploaded_file.txt'
s3_client.upload_file(file_path, bucket_name, key_name)
print(f"File {file_path} uploaded as {key_name}")

# Download a file
download_path = 'downloaded_file.txt'
s3_client.download_file(bucket_name, key_name, download_path)
print(f"File {key_name} downloaded as {download_path}")
