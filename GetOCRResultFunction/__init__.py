import azure.functions as func
import pyodbc, os, json

def main(req: func.HttpRequest) -> func.HttpResponse:
    image_id = req.params.get("id")

    conn = pyodbc.connect(os.environ["DB_CONN_STRING"])
    cur = conn.cursor()
    cur.execute("""
        SELECT ExtractedText, Language, Confidence
        FROM ImageOCRMetadata
        WHERE ImageName = ?
    """, image_id)

    row = cur.fetchone()

    return func.HttpResponse(
        json.dumps({
            "text": row[0],
            "language": row[1],
            "confidence": row[2]
        }),
        mimetype="application/json"
    )
