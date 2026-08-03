from database.scripts.db_connection import get_connection
from database.scripts.s3_connection import list_all_images
from database.scripts.aws_config import *

def insert_uploaded_documents():

    images = list_all_images()

    if not images:
        print("No images found in S3.")
        return

    conn = get_connection()

    cur = conn.cursor()

    inserted = 0

    for image in images:

        object_key = image["Key"]

        # Skip folder entry
        if object_key.endswith("/"):
            continue

        image_name = object_key.split("/")[-1]

        # Extract page number if filename contains page_x
        try:
            page_number = int(
                image_name.split("_")[-1]
                .replace(".jpg", "")
                .replace(".png", "")
                .replace(".jpeg", "")
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
        ON CONFLICT (object_key) DO NOTHING;
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

        inserted += 1

    conn.commit()

    cur.close()

    conn.close()

    print(f"{inserted} images inserted successfully.")


# ----------------------------------------------------
# Pipeline Function
# ----------------------------------------------------

def process_uploaded_documents():

    insert_uploaded_documents()


if __name__ == "__main__":

    process_uploaded_documents()