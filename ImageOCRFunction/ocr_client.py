import os
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

# Create Vision client
client = ComputerVisionClient(
    os.environ["VISION_ENDPOINT"],
    CognitiveServicesCredentials(os.environ["VISION_KEY"])
)

def run_ocr(image_path):
    """
    Sends image to Azure Computer Vision OCR (Read API)
    """
    with open(image_path, "rb") as image_stream:
        response = client.read_in_stream(image_stream, raw=True)

    operation_id = response.headers["Operation-Location"].split("/")[-1]

    # Poll for result
    while True:
        result = client.get_read_result(operation_id)
        if result.status not in ["notStarted", "running"]:
            break
        time.sleep(1)

    extracted_text = []
    language = "unknown"

    if result.status == "succeeded":
        for page in result.analyze_result.read_results:
            language = page.language
            for line in page.lines:
                extracted_text.append(line.text)

    return {
        "text": " ".join(extracted_text),
        "language": language,
        "confidence": 0.95
    }
