
from flask import Flask, render_template, request, jsonify
import voyageai
from PIL import Image
from pymongo import MongoClient
import io
import os
import numpy as np

app = Flask(__name__)

# Initialize clients
vo = voyageai.Client()
client = MongoClient(os.environ['MONGODB_URI'])
db = client['celebrity_db']
collection = db['celebrity_images']

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

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
        
        # Get embedding for uploaded image
        inputs = [[image]]
        print("Getting embedding...")
        result = vo.multimodal_embed(inputs, model="voyage-multimodal-3")
        query_embedding = result.embeddings[0]
        print("Got embedding successfully")
        
        # Use MongoDB vector search
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_search",
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
        
        # Execute search and format results
        print("Executing MongoDB search...")
        results = list(collection.aggregate(pipeline))
        print(f"Found {len(results)} results")
        
        top_3 = [{
            'name': doc['name'],
            'similarity': float(doc['similarity']),
            's3_url': doc['s3_url']
        } for doc in results]
        
        print(f"Returning results: {top_3}")
        return jsonify(top_3)
        
    except Exception as e:
        print(f"Error in search endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
