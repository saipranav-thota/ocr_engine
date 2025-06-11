from langchain_community.document_loaders.mongodb import MongodbLoader

loader = MongodbLoader(
    connection_string="mongodb://localhost:27017/",
    db_name="appdb",
    collection_name="documents",  
    field_names=["text_", "document_id"],
)

documents = loader.load()
text_body = documents[1].page_content
content, doc_id = text_body.rsplit(' ', 1)



if __name__ == "__main__":
    print("Document ID:", doc_id)
    print("Content:", content)