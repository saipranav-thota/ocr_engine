import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv() 

def insert_data_to_mongo(metadata: dict,  data: dict, db_name=None, collection_name=None):
    try:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        db_name = db_name or os.getenv("DB_NAME", "ocr_test")
        collection_name = collection_name or os.getenv("COLLECTION_NAME", "image_metadata")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        document = {**metadata, **data}
        result = collection.insert_one(document)

        logging.info(f"Inserted document with _id: {result.inserted_id}")
        return result.inserted_id

    except Exception as e:
        logging.error(f"Failed to insert metadata into MongoDB: {e}")
        return None
