from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
from main import main  
app = FastAPI()

@app.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    try:
        # Save uploaded file to local disk
        file_path = file.filename
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Call your main processing function
        main(file_path)

        # # Optional: Remove the file afterward if not needed
        # os.remove(file_path)

        return {"status": "success", "message": "Image processed and metadata stored."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "detail": str(e)})
