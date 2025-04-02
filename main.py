
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
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    image = Image.open(image_file)
    
    # Get embedding for uploaded image
    inputs = [["An image of a person", image]]
    result = vo.multimodal_embed(inputs, model="voyage-multimodal-3")
    query_embedding = result.embeddings[0]
    
    # Find similar celebrities
    all_celebs = list(collection.find())
    similarities = []
    
    for celeb in all_celebs:
        if 'embedding' in celeb:
            similarity = cosine_similarity(query_embedding, celeb['embedding'])
            similarities.append({
                'name': celeb['name'],
                'similarity': float(similarity),
                's3_url': celeb['s3_url']
            })
    
    # Sort by similarity and get top 3
    similarities.sort(key=lambda x: x['similarity'], reverse=True)
    top_3 = similarities[:3]
    
    return jsonify(top_3)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
