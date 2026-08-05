import os
import boto3

from dotenv import load_dotenv
from botocore.exceptions import ClientError

from app.services.pdf_service import convert_pdf_to_images

from app.services.json_service import (
    process_invoice_to_json
)

load_dotenv()

bucket = os.getenv("AWS_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

UPLOAD_PDF_FOLDER = "uploads/pdfs"
UPLOAD_IMAGE_FOLDER = "uploads/images"


# ==========================================================
# Upload PDF
# ==========================================================

def upload_pdf(local_pdf_path, filename):

    s3_key = f"invoices/{filename}"

    s3.upload_file(
        local_pdf_path,
        bucket,
        s3_key
    )

    return s3_key


# ==========================================================
# Upload Image
# ==========================================================

def upload_image(local_image_path):

    image_name = os.path.basename(local_image_path)

    s3_key = f"converted_images/{image_name}"

    s3.upload_file(
        local_image_path,
        bucket,
        s3_key
    )

    return s3_key

# ==========================================================
# Main Upload Controller
# ==========================================================

def upload_to_s3(file):

    filename = file.filename

    extension = filename.split(".")[-1].lower()

    image_extensions = [
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "tiff",
        "webp"
    ]

    # -------------------------
    # IMAGE
    # -------------------------

    if extension in image_extensions:

        file_type = "image"

        local_path = os.path.join(
            UPLOAD_IMAGE_FOLDER,
            filename
        )

        with open(local_path, "wb") as f:
            f.write(file.file.read())

        s3_key = upload_image(local_path)

        # -----------------------------
        # OCR + JSON
        # -----------------------------

        json_response = process_invoice_to_json(
            image_paths=[local_path],
            original_filename=filename
        )

        # return {

        #     "status": "success",

        #     "message": "File Uploaded Successfully",

        #     "filename": filename,

        #     "file_type": file_type,

        #     "extension": extension,

        #     "s3_bucket": bucket,

        #     "s3_key": s3_key,

        #     "converted_images": [
        #         s3_key
        #     ],

        #     "json_s3_key": json_response["json_s3_key"]

        # }

        return {

            "status": "success",

            "message": "File Uploaded Successfully",

            "filename": filename,

            "image_name": os.path.basename(s3_key),

            "file_type": file_type,

            "extension": extension,

            "s3_bucket": bucket,

            "s3_key": s3_key,

            "converted_images": [
                s3_key
            ],

            "json_s3_key": json_response["json_s3_key"]

        }
    # -------------------------
    # PDF
    # -------------------------

    elif extension == "pdf":

        file_type = "pdf"

        local_pdf_path = os.path.join(
            UPLOAD_PDF_FOLDER,
            filename
        )

        with open(local_pdf_path, "wb") as f:
            f.write(file.file.read())

        pdf_s3_key = upload_pdf(
            local_pdf_path,
            filename
        )

        # Convert PDF to Images

        image_paths = convert_pdf_to_images(
            local_pdf_path
        )

        uploaded_images = []

        for image in image_paths:

            uploaded_images.append(
                upload_image(image)
            )

        # -----------------------------
        # OCR + ONE JSON
        # -----------------------------

        json_response = process_invoice_to_json(
            image_paths=image_paths,
            original_filename=filename
        )

        image_name = os.path.basename(uploaded_images[0]) 

        # return {

        #     "status": "success",

        #     "message": "File Uploaded Successfully",

        #     "filename": filename,

        #     "file_type": file_type,

        #     "extension": extension,

        #     "s3_bucket": bucket,

        #     "s3_key": pdf_s3_key,

        #     #"converted_images": uploaded_images,
        #     "image_name": os.path.basename(s3_key),

        #     "json_s3_key": json_response["json_s3_key"]

        # }  

        return {

            "status": "success",

            "message": "File Uploaded Successfully",

            "filename": filename,

            "image_name": image_name,

            "file_type": file_type,

            "extension": extension,

            "s3_bucket": bucket,

            "s3_key": pdf_s3_key,

            "converted_images": uploaded_images,

            "json_s3_key": json_response["json_s3_key"]

        }


# ==========================================================
# LIST
# ==========================================================

def list_invoices():

    response = s3.list_objects_v2(
        Bucket=bucket,
        Prefix="converted_images/"
    )

    invoices = []

    if "Contents" in response:

        for obj in response["Contents"]:

            invoices.append({

                "filename": obj["Key"].split("/")[-1],

                "size": obj["Size"],

                "last_modified": str(obj["LastModified"])
            })

    return {

        "status": "success",

        "total_files": len(invoices),

        "invoices": invoices
    }


# ==========================================================
# GET
# ==========================================================

def get_invoice(filename):

    s3_key = f"invoices/{filename}"

    try:

        response = s3.head_object(
            Bucket=bucket,
            Key=s3_key
        )

        extension = filename.split(".")[-1].lower()

        if extension == "pdf":
            file_type = "pdf"
        else:
            file_type = "image"

        return {

            "status": "success",

            "filename": filename,

            "file_type": file_type,

            "extension": extension,

            "size": response["ContentLength"],

            "content_type": response["ContentType"],

            "last_modified": str(response["LastModified"]),

            "s3_bucket": bucket,

            "s3_key": s3_key
        }

    except ClientError:

        return {

            "status": "failed",

            "message": "Invoice Not Found"
        }


# ==========================================================
# DELETE
# ==========================================================

# ==========================================================
# DELETE
# ==========================================================

def delete_invoice(filename):

    extension = filename.split(".")[-1].lower()

    image_extensions = [
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "tiff",
        "webp"
    ]

    try:

        # =====================================================
        # PDF
        # =====================================================

        if extension == "pdf":

            pdf_key = f"invoices/{filename}"

            s3.delete_object(
                Bucket=bucket,
                Key=pdf_key
            )

            base_name = os.path.splitext(filename)[0]

            # -----------------------------------------
            # Delete Converted Images
            # -----------------------------------------

            image_response = s3.list_objects_v2(
                Bucket=bucket,
                Prefix=f"converted_images/{base_name}"
            )

            if "Contents" in image_response:

                for obj in image_response["Contents"]:

                    s3.delete_object(
                        Bucket=bucket,
                        Key=obj["Key"]
                    )

            # -----------------------------------------
            # Delete OCR JSON Files
            # -----------------------------------------

            json_response = s3.list_objects_v2(
                Bucket=bucket,
                Prefix=f"ocr_json/{base_name}"
            )

            if "Contents" in json_response:

                for obj in json_response["Contents"]:

                    s3.delete_object(
                        Bucket=bucket,
                        Key=obj["Key"]
                    )

        # =====================================================
        # IMAGE
        # =====================================================

        elif extension in image_extensions:

            image_key = f"converted_images/{filename}"

            s3.delete_object(
                Bucket=bucket,
                Key=image_key
            )

            base_name = os.path.splitext(filename)[0]

            # -----------------------------------------
            # Delete OCR JSON
            # -----------------------------------------

            json_response = s3.list_objects_v2(
                Bucket=bucket,
                Prefix=f"ocr_json/{base_name}"
            )

            if "Contents" in json_response:

                for obj in json_response["Contents"]:

                    s3.delete_object(
                        Bucket=bucket,
                        Key=obj["Key"]
                    )

        # =====================================================
        # Unsupported
        # =====================================================

        else:

            return {
                "status": "failed",
                "message": "Unsupported File Type"
            }

        return {

            "status": "success",

            "message": "Invoice Deleted Successfully",

            "filename": filename

        }

    except ClientError:

        return {

            "status": "failed",

            "message": "Invoice Not Found"

        }
    