from ocr_extraction import analyze_image_from_url
from upload import upload_image_to_blob



local_image_path = "handwritten.png"
analyze_image_from_url(upload_image_to_blob(local_image_path))
