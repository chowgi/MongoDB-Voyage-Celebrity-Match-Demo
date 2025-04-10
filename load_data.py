
import json
import os
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from pymongo.errors import BulkWriteError
from bson import json_util, ObjectId

def load_celebrity_data():
    # Get MongoDB URI from environment variable
    mongodb_uri = os.environ.get('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("Please set the MONGODB_URI environment variable")

    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    db = client['celebrity_db']
    collection = db['celebrity_images']

    # Read JSON data using json_util to properly handle MongoDB extended JSON
    with open('celebrity_images.json', 'r') as f:
        celebrities = json_util.loads(f.read())

    # Remove _id field to let MongoDB auto-generate it and check for existing documents
    new_celebrities = []
    for celebrity in celebrities:
        # Check if document already exists
        if not collection.find_one({"name": celebrity.get("name")}):
            if '_id' in celebrity:
                del celebrity['_id']
            new_celebrities.append(celebrity)
        else:
            print(f"Skipping {celebrity.get('name')} - Document already exists")

    if new_celebrities:
        try:
            # Insert only new documents
            result = collection.insert_many(new_celebrities)
            print(f"Successfully inserted {len(result.inserted_ids)} documents")
        except BulkWriteError as e:
            print(f"Error inserting documents: {e.details}")
        finally:
            client.close()
    else:
        print("No new documents to insert")

def create_index():
    # Get MongoDB URI from environment variable
    mongodb_uri = os.environ.get('MONGODB_URI')
    if not mongodb_uri:
        raise ValueError("Please set the MONGODB_URI environment variable")

    # Connect to MongoDB
    client = MongoClient(mongodb_uri)
    db = client['celebrity_db']
    collection = db['celebrity_images']

    # Create vector search index if it doesn't exist
    try:
        # List all search indexes
        existing_indexes = collection.list_search_indexes()
        index_exists = any(index['name'] == 'vector_index' for index in existing_indexes)
        
        if not index_exists:
            search_model = SearchIndexModel(
                definition={
                  "fields": [
                    {
                      "numDimensions": 1024,
                      "path": "embedding",
                      "similarity": "cosine",
                      "type": "vector"
                    }
                  ]
                },
                name="vector_index",
                type="vectorSearch"
            )
            collection.create_search_index(search_model)
            print("Created vector search index")
        else:
            print("Vector search index already exists")
    except Exception as e:
        print(f"Error managing search index: {str(e)}")

if __name__ == "__main__":
    load_celebrity_data()
    create_index()
