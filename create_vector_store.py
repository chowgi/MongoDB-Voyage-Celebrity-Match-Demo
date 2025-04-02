
import os
import boto3
from pymongo import MongoClient
import voyageai
from PIL import Image
import io

# Initialize clients
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ['aws_access_key'],
    aws_secret_access_key=os.environ['aws_secret_key'],
    region_name="ap-south-1"
)
bucket_name = 'celeb-images-demo'

# Initialize Voyage client
vo = voyageai.Client()  # Uses VOYAGE_API_KEY environment variable

# Connect to MongoDB
client = MongoClient(os.environ['MONGODB_URI'])
db = client['celebrity_db']
collection = db['celebrity_images']

def get_image_from_s3(celebrity, image_key):
    """Get image from S3 and return as PIL Image"""
    response = s3_client.get_object(Bucket=bucket_name, Key=f"{celebrity}/{image_key}")
    image_bytes = response['Body'].read()
    return Image.open(io.BytesIO(image_bytes))

def process_celebrity_images():
    """Process all celebrity images and create vector embeddings"""
    paginator = s3_client.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=bucket_name, Delimiter='/'):
        for prefix in page.get('CommonPrefixes', []):
            celebrity_name = prefix.get('Prefix').rstrip('/')
            
            # Get first image only
            celebrity_images = s3_client.list_objects_v2(
                Bucket=bucket_name,
                Prefix=prefix.get('Prefix'),
                MaxKeys=1
            )
            
            try:
                # Get the first image
                first_image = celebrity_images.get('Contents', [])[0]
                image_key = first_image['Key'].split('/')[-1]
                s3_url = f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{first_image['Key']}"
                
                # Get image from S3 as PIL Image
                pil_image = get_image_from_s3(celebrity_name, image_key)
                
                # Create input for embedding
                inputs = [[f"An image of {celebrity_name}", pil_image]]
                
                # Get embedding using Voyage AI
                result = vo.multimodal_embed(inputs, model="voyage-multimodal-3")
                embedding = result.embeddings[0]
                
                # Update document with first image info and embedding at root level
                collection.update_one(
                    {'name': celebrity_name},
                    {
                        '$set': {
                            'name': celebrity_name,
                            'image_key': image_key,
                            's3_url': s3_url,
                            'embedding': embedding
                        }
                    },
                    upsert=True
                )
                print(f"Processed {image_key} for {celebrity_name}")
                    
            except Exception as e:
                print(f"Error processing images for {celebrity_name}: {str(e)}")
                continue

if __name__ == "__main__":
    process_celebrity_images()
