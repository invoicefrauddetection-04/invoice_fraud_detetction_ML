import json

from database.scripts.db_connection import get_connection
from database.scripts.s3_connection import get_s3_client
from database.scripts.aws_config import *

# Import the parser
from predictions.parse_ocr_json import parse_ocr_json


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
# Get document_id
# ----------------------------------------------------

def get_document_id(cur, image_name):

    cur.execute(
        """
        SELECT document_id
        FROM uploaded_documents
        WHERE image_name = %s;
        """,
        (image_name,)
    )

    row = cur.fetchone()

    if row:
        return row[0]

    return None


# ----------------------------------------------------
# Insert OCR Result
# ----------------------------------------------------

def insert_ocr_result(bucket_name, object_key):

    # Read OCR JSON
    ocr_json = read_json_from_s3(
        bucket_name,
        object_key
    )

    # Parse OCR JSON
    invoice = parse_ocr_json(ocr_json)

    print("\nAfter Parser:")
    print(invoice["total_amount"])
    print(type(invoice["total_amount"]))

    print("\n========== Parsed Invoice ==========\n")

    for key, value in invoice.items():
        print(f"{key:20}: {value}")

    conn = get_connection()

    cur = conn.cursor()

    document_id = get_document_id(
        cur,
        invoice["image_name"]
    )

    if document_id is None:

        print("Document not found.")

        cur.close()
        conn.close()

        return

    invoice["document_id"] = document_id

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

    print("\nBefore INSERT:")
    print(invoice)

    cur.execute(query, invoice)

    conn.commit()

    print("\nOCR Result saved successfully.")

    cur.execute(
        """
        SELECT *
        FROM ocr_results
        WHERE document_id = %s;
        """,
        (document_id,)
    )
    

    print("\n========== Database Record ==========")

    print(cur.fetchone())

    cur.close()

    conn.close()


# ----------------------------------------------------
# Main
# ----------------------------------------------------

if __name__ == "__main__":

    insert_ocr_result(
        bucket_name=BUCKET_NAME,
        object_key="ocr_json/Invoice_009.json"
    )
