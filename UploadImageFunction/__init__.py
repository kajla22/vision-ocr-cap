import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("UploadImageFunction triggered.")

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    # Handle preflight (IMPORTANT for web hosting)
    if req.method == "OPTIONS":
        return func.HttpResponse("", status_code=204, headers=headers)

    try:
        file = req.files.get("file")

        if not file:
            return func.HttpResponse(
                json.dumps({"error": "No file provided"}),
                status_code=400,
                headers=headers,
                mimetype="application/json"
            )

        conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
        blob_service = BlobServiceClient.from_connection_string(conn_str)

        container_name = "images"
        blob_client = blob_service.get_blob_client(container_name, file.filename)

        blob_client.upload_blob(file.stream, overwrite=True)

        blob_url = blob_client.url

        return func.HttpResponse(
            json.dumps({
                "message": "Upload successful",
                "blobUrl": blob_url
            }),
            status_code=200,
            headers=headers,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            headers=headers,
            mimetype="application/json"
        )
