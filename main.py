from flask import Flask, render_template, request, jsonify
import voyageai
from PIL import Image
from pymongo import MongoClient
import boto3
import io
import os
import numpy as np
import base64

app = Flask(__name__)

def get_image_from_s3(bucket_name, key):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        image_data = response['Body'].read()
        return base64.b64encode(image_data).decode('utf-8')
    except Exception as e:
        print(f"Error getting image from S3: {str(e)}")
        return None

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ['aws_access_key'],
    aws_secret_access_key=os.environ['aws_secret_key'],
    region_name="ap-south-1"
)

# Initialize clients
vo = voyageai.Client()
client = MongoClient(os.environ['MONGODB_URI'])
db = client['celebrity_db']
collection = db['celebrity_images']

# Verify vector search index exists
indexes = collection.list_indexes()
vector_index_exists = any('vector_index' in idx.get('name', '') for idx in indexes)
if not vector_index_exists:
    print("Warning: vector_search index not found in MongoDB collection")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        if 'image' not in request.files:
            print("No image file in request")
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        print(f"Received image: {image_file.filename}")

        image = Image.open(image_file)
        print("Successfully opened image")

        # Get embedding for uploaded image - match format used in vector store
        inputs = [["An image of a Brad Pitt", image]]
        print("Getting embedding...")
        result = vo.multimodal_embed(inputs, model="voyage-multimodal-3")
        query_embedding = result.embeddings[0]
        print(f"Embedding shape: {len(query_embedding)}")
        print("First 10 values of embedding:", query_embedding[:10])
        print("Min value:", min(query_embedding))
        print("Max value:", max(query_embedding))
        print("Average value:", sum(query_embedding) / len(query_embedding))

        # Use MongoDB vector search
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "queryVector": query_embedding,
                    "path": "embedding",
                    "numCandidates": 100,
                    "limit": 3
                }
            },
            {
                "$project": {
                    "name": 1,
                    "s3_url": 1,
                    "similarity": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        # Verify collection has data
        total_docs = collection.count_documents({})
        print(f"Total documents in collection: {total_docs}")

        # Execute search and format results
        print("Executing MongoDB search...")
        results = list(collection.aggregate(pipeline))
        print(f"Found {len(results)} results")

        top_3 = []
        for doc in results:
            image_key = f"{doc['name']}/image_1.jpg"
            image_data = get_image_from_s3('celeb-images-demo', image_key)
            if image_data:
                top_3.append({
                    'name': doc['name'],
                    'similarity': float(doc['similarity']),
                    'image_data': image_data
                })

        print(f"Returning results: {top_3}")
        return jsonify(top_3)

    except Exception as e:
        print(f"Error in search endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)