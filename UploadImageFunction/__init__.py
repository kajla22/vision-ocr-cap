import logging
import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os
import uuid

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("UploadImageFunction triggered.")

    try:
        file = req.files.get('file')
        logging.info(f"Received file: {file.filename if file else 'NO FILE'}")

        if not file:
            return func.HttpResponse(
                json.dumps({"error": "No file provided"}),
                status_code=400,
                mimetype="application/json"
            )

        conn_str = os.environ.get("STORAGE_CONNECTION_STRING")
        if not conn_str:
            return func.HttpResponse(
                json.dumps({"error": "Storage connection string not configured"}),
                status_code=500,
                mimetype="application/json"
            )

        # Optional: make filename unique
        filename = f"{uuid.uuid4()}_{file.filename}"

        blob_service = BlobServiceClient.from_connection_string(conn_str)
        container_name = "images"

        blob_client = blob_service.get_blob_client(container_name, filename)
        blob_client.upload_blob(file.stream, overwrite=True)

        # ✅ RETURN JSON (THIS IS THE KEY)
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "imageName": filename
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
