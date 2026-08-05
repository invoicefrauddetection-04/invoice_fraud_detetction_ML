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
# Get Uploaded Document
# ----------------------------------------------------

def get_uploaded_document(cur, document_id):

    query = """
        SELECT document_id, image_name
        FROM uploaded_documents
        WHERE document_id = %s
        AND processing_status = 'UPLOADED';
    """

    cur.execute(query, (document_id,))

    return cur.fetchone()


# ----------------------------------------------------
# Insert OCR Result
# ----------------------------------------------------

def insert_ocr_result(bucket_name, document_id):

    conn = get_connection()
    cur = conn.cursor()

    row = get_uploaded_document(cur, document_id)

    if row is None:

        print(f"Document {document_id} not found or already processed.")

        cur.close()
        conn.close()

        return

    document_id, image_name = row

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

    try:

        print("\n======================================")
        print(f"Processing Document ID : {document_id}")
        print("======================================")

        object_key = get_json_object_key(image_name)

        print(f"Image Name : {image_name}")
        print(f"OCR JSON   : {object_key}")

        print("\nTrying to fetch S3 object:")
        print(f"Bucket : {bucket_name}")
        print(f"Key    : {object_key}")

        ocr_json = read_json_from_s3(
            bucket_name,
            object_key
        )

        invoice = parse_ocr_json(ocr_json)

        invoice["document_id"] = document_id

        print("\n========== Parsed Invoice ==========\n")

        for key, value in invoice.items():
            print(f"{key:20}: {value}")

        cur.execute(query, invoice)

        cur.execute(
            """
            UPDATE uploaded_documents
            SET processing_status = 'OCR_COMPLETED'
            WHERE document_id = %s;
            """,
            (document_id,)
        )

        conn.commit()

        print(f"\n✓ OCR Result saved for Document {document_id}")

    except Exception as e:

        conn.rollback()

        print(f"\n✗ Failed to process Document {document_id}")
        print(f"{type(e).__name__}: {e}")

    finally:

        cur.close()
        conn.close()


# ----------------------------------------------------
# Pipeline Function
# ----------------------------------------------------

def process_ocr(document_id):

    insert_ocr_result(
        BUCKET_NAME,
        document_id
    )

'''
# ----------------------------------------------------
# Testing Purpose Only
# ----------------------------------------------------

if __name__ == "__main__":

    try:

        document_id = int(input("Enter Document ID: "))
        process_ocr(document_id)

    except ValueError:

        print("Please enter a valid Document ID.")
'''