
import boto3
import requests
from PIL import Image
import io
import os

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ['aws_access_key'],
    aws_secret_access_key=os.environ['aws_secret_key'],
    region_name="ap-south-1"
)

def test_direct_url():
    print("Testing direct URL access...")
    url = "https://celeb-images-demo.s3.ap-south-1.amazonaws.com/Brad+Pitt/image_1.jpg"
    response = requests.get(url)
    if response.status_code == 200:
        print("✓ Direct URL access successful")
        # Try to open image to verify it's valid
        image = Image.open(io.BytesIO(response.content))
        print("✓ Image successfully loaded")
        print(f"Image size: {image.size}")
    else:
        print(f"✗ Direct URL access failed with status code: {response.status_code}")

def test_s3_access():
    print("\nTesting S3 API access...")
    try:
        response = s3_client.get_object(
            Bucket='celeb-images-demo',
            Key='Brad Pitt/image_1.jpg'
        )
        image = Image.open(response['Body'])
        print("✓ S3 API access successful")
        print(f"Image size: {image.size}")
    except Exception as e:
        print(f"✗ S3 API access failed with error: {str(e)}")

if __name__ == "__main__":
    test_direct_url()
    test_s3_access()
