from pymongo import MongoClient

client = MongoClient()
db = client["appdb"]
collection = db["documents"]


def loader_data(doc_id, path, field, text_data):
    for f,d in zip(field, text_data):
        update_path = f"{path}.{f}"
        collection.update_one(
            {"document_id": doc_id},
            {"$set": {update_path: d}}
        )