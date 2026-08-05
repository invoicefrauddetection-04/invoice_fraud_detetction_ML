from app.pipeline_DB.database.scripts.db_connection import get_connection
from app.pipeline_DB.database.scripts.s3_connection import list_all_images
from app.pipeline_DB.database.scripts.aws_config import *


def insert_uploaded_documents():

    images = list_all_images()

    if not images:
        print("No images found in S3.")
        return None

    conn = get_connection()
    cur = conn.cursor()

    inserted = 0
    latest_document_id = None

    for image in images:

        object_key = image["Key"]

        # Skip folder entries
        if object_key.endswith("/"):
            continue

        image_name = object_key.split("/")[-1]

        try:
            page_number = int(
                image_name.split("_")[-1]
                .replace(".jpg", "")
                .replace(".jpeg", "")
                .replace(".png", "")
            )
        except:
            page_number = 1

        upload_time = image["LastModified"]

        query = """
        INSERT INTO uploaded_documents
        (
            image_name,
            page_number,
            bucket_name,
            object_key,
            upload_timestamp,
            processing_status
        )
        VALUES
        (%s,%s,%s,%s,%s,%s)

        ON CONFLICT (object_key)
        DO NOTHING

        RETURNING document_id;
        """

        cur.execute(

            query,

            (

                image_name,
                page_number,
                BUCKET_NAME,
                object_key,
                upload_time,
                "UPLOADED"

            )

        )

        row = cur.fetchone()

        if row:

            latest_document_id = row[0]
            inserted += 1

    conn.commit()

    cur.close()
    conn.close()

    print(f"{inserted} images inserted successfully.")

    return latest_document_id


# ----------------------------------------------------
# Pipeline Function
# ----------------------------------------------------

def process_uploaded_documents():

    return insert_uploaded_documents()


if __name__ == "__main__":

    document_id = process_uploaded_documents()

    print(f"\nLatest Document ID : {document_id}")