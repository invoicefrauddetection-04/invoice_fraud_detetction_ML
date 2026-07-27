import os
import json
import boto3
from dotenv import load_dotenv

from app.services.ocr_service import extract_text

load_dotenv()

bucket = os.getenv("AWS_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

JSON_FOLDER = "uploads/json"

os.makedirs(JSON_FOLDER, exist_ok=True)


# ==========================================================
# Build Invoice JSON
# ==========================================================

def build_invoice_json(original_filename, image_paths):

    pages = []

    for page_number, image_path in enumerate(image_paths, start=1):

        ocr_result = extract_text(image_path)

        page_data = {
            "page": page_number,
            "image_name": os.path.basename(image_path),
            "ocr": ocr_result
        }

        pages.append(page_data)

    invoice_json = {

        "invoice_name": original_filename,

        "total_pages": len(image_paths),

        "pages": pages

    }

    return invoice_json


# ==========================================================
# Save JSON Locally
# ==========================================================

def save_json_locally(invoice_json):

    filename = os.path.splitext(
        invoice_json["invoice_name"]
    )[0] + ".json"

    json_path = os.path.join(
        JSON_FOLDER,
        filename
    )

    with open(json_path, "w", encoding="utf-8") as f:

        json.dump(
            invoice_json,
            f,
            indent=4,
            ensure_ascii=False
        )

    return json_path


# ==========================================================
# Process Complete Invoice
# ==========================================================

def process_invoice_to_json(image_paths, original_filename):

    # Build JSON from all pages
    invoice_json = build_invoice_json(
        original_filename,
        image_paths
    )

    # Save locally
    json_path = save_json_locally(
        invoice_json
    )

    # Upload JSON to S3
    json_filename = os.path.basename(json_path)

    json_s3_key = f"ocr_json/{json_filename}"

    s3.upload_file(
        json_path,
        bucket,
        json_s3_key
    )

    return {

        "json_local_path": json_path,

        "json_s3_key": json_s3_key,

        "invoice_json": invoice_json

    }