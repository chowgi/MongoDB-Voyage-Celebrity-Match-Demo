from flask import Flask, render_template, request, jsonify
import voyageai
from PIL import Image
from pymongo import MongoClient
import requests
import os
import base64

app = Flask(__name__)

def get_image_from_s3(bucket_name, key):
    try:
        url = f"https://{bucket_name}.s3.ap-south-1.amazonaws.com/{key}"
        response = requests.get(url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode('utf-8')
        return None
    except Exception as e:
        print(f"Error getting image from S3: {str(e)}")
        return None

# Initialize clients
vo = voyageai.Client()
client = MongoClient(os.environ['MONGODB_URI'])
db = client['celebrity_db']
collection = db['celebrity_images']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image_file = request.files['image']
        image = Image.open(image_file)

        # Get embedding for uploaded image
        inputs = [["Focus on facial geometry, proportions, and distinguishing features, such as jawline structure, cheekbone prominence, or the relative positioning of facial elements like eyes, nose, and mouth.", image]]
        result = vo.multimodal_embed(inputs, model="voyage-multimodal-3")
        query_embedding = result.embeddings[0]

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

        results = list(collection.aggregate(pipeline))
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

        return jsonify(top_3)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)