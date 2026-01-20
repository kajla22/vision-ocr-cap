import os
import pyodbc
from azure.storage.blob import BlobServiceClient
from .ocr_client import run_ocr

def process_image(image_url):
    blob_name = image_url.split("/")[-1]
    path = f"/tmp/{blob_name}"

    blob = BlobServiceClient.from_connection_string(
        os.environ["STORAGE_CONNECTION_STRING"]
    ).get_blob_client("images", blob_name)

    with open(path, "wb") as f:
        f.write(blob.download_blob().readall())

    result = run_ocr(path)

    conn = pyodbc.connect(os.environ["DB_CONN_STRING"])
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO ImageOCRMetadata
        (ImageName, ExtractedText, Language, Confidence)
        VALUES (?, ?, ?, ?)
    """, blob_name, result["text"], result["language"], result["confidence"])
    conn.commit()
    conn.close()
