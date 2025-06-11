import os
import time
from dotenv import load_dotenv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

load_dotenv()

VISION_ENDPOINT = os.getenv("VISION_ENDPOINT")
VISION_KEY = os.getenv("VISION_KEY")

if not VISION_ENDPOINT or not VISION_KEY:
    raise Exception("Please set VISION_ENDPOINT and VISION_KEY in .env")


vision_client = ComputerVisionClient(VISION_ENDPOINT, CognitiveServicesCredentials(VISION_KEY))



def analyze_image_from_url(image_url):
    response = vision_client.read(image_url, raw=True)
    operation_location = response.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    while True:
        result = vision_client.get_read_result(operation_id)
        if result.status.lower() in ["succeeded", "failed"]:
            break
        time.sleep(1)

    if result.status.lower() == "succeeded":
        text = ""
        for page in result.analyze_result.read_results:
            for line in page.lines:
                text += line.text + "\n"
        print("OCR Text:\n", text)
        return text
    else:
        print("OCR failed.")
        return None