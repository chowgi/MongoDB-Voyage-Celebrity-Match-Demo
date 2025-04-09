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

    # Clean the documents to ensure proper ObjectId handling
    for celebrity in celebrities:
        if '_id' in celebrity and isinstance(celebrity['_id'], dict):
            if '$oid' in celebrity['_id']:
                celebrity['_id'] = ObjectId(celebrity['_id']['$oid'])

    try:
        # Insert the data
        result = collection.insert_many(celebrities)
        print(f"Successfully inserted {len(result.inserted_ids)} documents")

        # Check for existing vector search index
        index_exists = False
        for index in collection.list_search_indexes():  # Use list_search_indexes() instead of list_indexes()
            if index.get('name') == 'vector_index':
                index_exists = True
                break

        # Create index if not exists
        
        if not index_exists:
            search_model = SearchIndexModel(
                definition={
                    "mappings": {
                        "fields": [
                            {
                                "type": "vector",
                                "path": "embeddings",
                                "numDimensions": 1024,
                                "similarity": "cosine",
                            }
                        ],
                    }
                },
                name="vector_index",
                type="vectorSearch",
            )
            collection.create_search_index(search_model)

    except BulkWriteError as e:
        print(f"Error inserting documents: {e.details}")
    finally:
        client.close()

if __name__ == "__main__":
    load_celebrity_data()