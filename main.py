import logging
import os
from PIL import Image
import datetime
from ocr_extraction import analyze_image_from_url
from upload import upload_image_to_blob
from database import insert_data_to_mongo
from transform import pipeline
from text_extraction import extract_flashcards, extract_mcq_data



def main(img):
    try:
        image = Image.open(img)
        filename = os.path.basename(img)
        image_format = image.format or "UNKNOWN"
        size = os.path.getsize(img)
        blob_url = upload_image_to_blob(img)
        now = datetime.datetime.utcnow().isoformat()

        metadata = {
            "info": {
                "filename": filename,
                "format": image_format,
                "size": size,
                "location": blob_url
            },
            "created_at": now,
            "updated_at": now
        }

        extracted_string = analyze_image_from_url(blob_url)

        result = pipeline(extracted_string)

        summary = result["summary"]
        flashcards = extract_flashcards(result["flashcard"])
        questions = extract_mcq_data(result["quiz"])


        

        data = {
            "extracted_string": extracted_string,
            "reinforcement_content": {
                "summary": summary,
                "flashcards": flashcards,
                "mcq": questions
            }
        }



        logging.info(f"Metadata structured (without OCR): {metadata}")
        logging.info(f"Text extracted using OCR: {data}")
        insert_data_to_mongo(metadata, data)
        logging.info("Metadata and Extracted text inserted into MongoDB successfully")

    except Exception as e:
        logging.error(f"Failed to process and store metadata: {e}")


if __name__  == "__main__":
    main("handwritten.png")