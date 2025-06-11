from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from upload import upload_image_to_blob
from ocr_extraction import analyze_image_from_url

app = FastAPI()

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    try:
        # Save uploaded file to local disk
        with open(file.filename, "wb") as buffer:
            buffer.write(await file.read())

        # Upload to Blob and get URL
        blob_url = upload_image_to_blob(file.filename)

        # Run OCR
        result = analyze_image_from_url(blob_url)

        return {"status": "success", "ocr_result": result}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
