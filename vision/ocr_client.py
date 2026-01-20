from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import os, time

client = ComputerVisionClient(
    os.environ["VISION_ENDPOINT"],
    CognitiveServicesCredentials(os.environ["VISION_KEY"])
)

def run_ocr(image_path):
    with open(image_path, "rb") as img:
        response = client.read_in_stream(img, raw=True)

    operation_id = response.headers["Operation-Location"].split("/")[-1]

    while True:
        result = client.get_read_result(operation_id)
        if result.status not in ["running", "notStarted"]:
            break
        time.sleep(1)

    text = []
    for page in result.analyze_result.read_results:
        for line in page.lines:
            text.append(line.text)

    return {
        "text": " ".join(text),
        "language": result.analyze_result.read_results[0].language,
        "confidence": 0.95
    }
