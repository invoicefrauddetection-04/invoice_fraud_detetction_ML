import json

from app.pipeline_DB.database.scripts.db_connection import get_connection
from app.pipeline_DB.database.scripts.s3_connection import get_s3_client
from app.pipeline_DB.database.scripts.aws_config import *

from app.pipeline_DB.predictions.parse_ocr_json import parse_ocr_json
from app.pipeline_DB.predictions.file_utils import get_json_object_key


# ----------------------------------------------------
# Read OCR JSON from S3
# ----------------------------------------------------

def read_json_from_s3(bucket_name, object_key):

    s3 = get_s3_client()

    response = s3.get_object(
        Bucket=bucket_name,
        Key=object_key
    )

    return json.loads(
        response["Body"].read().decode("utf-8")
    )


# ----------------------------------------------------
# Get All Uploaded Documents
# ----------------------------------------------------

def get_uploaded_documents(cur):

    cur.execute(
        """
        SELECT document_id, image_name
        FROM uploaded_documents
        WHERE processing_status = 'UPLOADED'
        ORDER BY document_id;
        """
    )

    return cur.fetchall()

# ----------------------------------------------------
# Insert OCR Result
# ----------------------------------------------------

def insert_ocr_result(bucket_name):

    conn = get_connection()
    cur = conn.cursor()

    # Get all uploaded documents
    rows = get_uploaded_documents(cur)

    if not rows:

        print("No new uploaded documents found.")

        cur.close()
        conn.close()

        return

    query = """
    INSERT INTO ocr_results
    (
        document_id,
        supplier_id,
        invoice_id,
        invoice_date,
        payment_terms,
        invoice_type,
        supplier_country,
        total_amount
    )
    VALUES
    (
        %(document_id)s,
        %(supplier_id)s,
        %(invoice_id)s,
        %(invoice_date)s,
        %(payment_terms)s,
        %(invoice_type)s,
        %(supplier_country)s,
        %(total_amount)s
    )

    ON CONFLICT (document_id)

    DO UPDATE SET

        supplier_id = EXCLUDED.supplier_id,
        invoice_id = EXCLUDED.invoice_id,
        invoice_date = EXCLUDED.invoice_date,
        payment_terms = EXCLUDED.payment_terms,
        invoice_type = EXCLUDED.invoice_type,
        supplier_country = EXCLUDED.supplier_country,
        total_amount = EXCLUDED.total_amount;
    """
    # Process every uploaded document
    for document_id, image_name in rows:

        try:

            print("\n======================================")
            print(f"Processing Document ID : {document_id}")
            print("======================================")

            # Generate OCR JSON path
            object_key = get_json_object_key(image_name)

            print(f"Image Name : {image_name}")
            print(f"OCR JSON   : {object_key}")

            print("\nTrying to fetch S3 object:")
            print(f"Bucket : {bucket_name}")
            print(f"Key    : {object_key}")
            
            # Read OCR JSON from S3
            ocr_json = read_json_from_s3(
                bucket_name,
                object_key
            )

            # Parse OCR JSON
            invoice = parse_ocr_json(ocr_json)
            invoice["document_id"] = document_id

            print("\n========== Parsed Invoice ==========\n")

            for key, value in invoice.items():
                print(f"{key:20}: {value}")

            # Insert / Update OCR Result
            cur.execute(query, invoice)

            # Update processing status
            cur.execute(
                """
                UPDATE uploaded_documents
                SET processing_status = 'OCR_COMPLETED'
                WHERE document_id = %s;
                """,
                (document_id,)
            )

            # Commit current document
            conn.commit()

            print(f"\n✓ OCR Result saved for Document {document_id}")

        except Exception as e:

            # Rollback only the failed transaction
            conn.rollback()

            print(f"\n✗ Failed to process Document {document_id}")
            print(f"{type(e).__name__}: {e}")

            continue

    print("\n======================================")
    print("All uploaded documents processed.")
    print("======================================")

    cur.close()
    conn.close()

# ----------------------------------------------------
# Pipeline Function
# ----------------------------------------------------

def process_ocr():

    insert_ocr_result(
        bucket_name=BUCKET_NAME
    )


# ----------------------------------------------------
# Testing Purpose Only
# ----------------------------------------------------

if __name__ == "__main__":

    process_ocr()