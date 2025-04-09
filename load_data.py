
import json
import os
from pymongo import MongoClient
from pymongo.errors import BulkWriteError

def load_celebrity_data():
    # Get MongoDB URI from environment variable
    mongodb_uri = os.environ.get('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("Please set the MONGODB_URI environment variable")

    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    db = client['celebrity_db']
    collection = db['celebrity_images']

    # Read JSON data
    with open('celebrity_images.json', 'r') as f:
        celebrities = json.load(f)

    try:
        # Insert the data
        result = collection.insert_many(celebrities)
        print(f"Successfully inserted {len(result.inserted_ids)} documents")
        
        # Create vector search index if it doesn't exist
        if "vector_index" not in collection.list_indexes():
            collection.create_index(
                [("embedding", "vectorSearch")],
                {
                    "numDimensions": 1024,
                    "similarity": "cosine"
                },
                name="vector_index"
            )
            print("Created vector search index")

    except BulkWriteError as e:
        print(f"Error inserting documents: {e.details}")
    finally:
        client.close()

if __name__ == "__main__":
    load_celebrity_data()
