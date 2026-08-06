# from app.pipeline_DB.database.scripts.db_connection import get_connection
# from app.pipeline_DB.database.scripts.s3_connection import list_all_images
# from app.pipeline_DB.database.scripts.aws_config import *


# # ----------------------------------------------------
# # Insert Uploaded Documents
# # ----------------------------------------------------

# def insert_uploaded_documents():

#     images = list_all_images()

#     if not images:

#         print("No images found in S3.")
#         return None

#     conn = get_connection()
#     cur = conn.cursor()

#     inserted = 0
#     latest_document_id = None
#     already_exists = False

#     try:

#         for image in images:

#             object_key = image["Key"]

#             # Skip folders
#             if object_key.endswith("/"):
#                 continue

#             image_name = object_key.split("/")[-1]

#             try:

#                 page_number = int(
#                     image_name.split("_")[-1]
#                     .replace(".jpg", "")
#                     .replace(".jpeg", "")
#                     .replace(".png", "")
#                 )

#             except Exception:

#                 page_number = 1

#             upload_time = image["LastModified"]

#             # ----------------------------------------------------
#             # Insert New Document
#             # ----------------------------------------------------

#             query = """
#                 INSERT INTO uploaded_documents
#                 (
#                     image_name,
#                     page_number,
#                     bucket_name,
#                     object_key,
#                     upload_timestamp,
#                     processing_status
#                 )
#                 VALUES
#                 (%s,%s,%s,%s,%s,%s)

#                 ON CONFLICT (object_key)
#                 DO NOTHING

#                 RETURNING document_id;
#             """

#             print("Bucket =", BUCKET_NAME)
#             print("Object =", object_key)
#             print("Image =", image_name)
            
#             cur.execute(

#                 query,

#                 (

#                     image_name,
#                     page_number,
#                     BUCKET_NAME,
#                     object_key,
#                     upload_time,
#                     "UPLOADED"

#                 )

#             )

#             row = cur.fetchone()

#             # -------------------------------
#             # New Invoice
#             # -------------------------------

#             if row:

#                 latest_document_id = row[0]

#                 inserted += 1

#                 already_exists = False

#                 print(f"✓ New Invoice Inserted : {image_name}")
#                 print(f"Document ID : {latest_document_id}")

#             # -------------------------------
#             # Existing Invoice
#             # -------------------------------

#             else:

#                 cur.execute(
#                     """
#                     SELECT
#                         document_id,
#                         processing_status
#                     FROM uploaded_documents
#                     WHERE object_key = %s;
#                     """,
#                     (object_key,)
#                 )

#                 existing = cur.fetchone()

#                 if existing:

#                     latest_document_id = existing[0]

#                     already_exists = True

#                     print(f"• Invoice Already Exists : {image_name}")
#                     print(f"Document ID : {latest_document_id}")
#                     print(f"Status      : {existing[1]}")

#         conn.commit()

#         print("\n===================================")
#         print(f"{inserted} New Invoice(s) Inserted")
#         print("===================================")

#         return latest_document_id, already_exists

#     except Exception as e:

#         conn.rollback()

#         print("\nFailed to insert uploaded document.")
#         print(e)

#         return None

#     finally:

#         cur.close()
#         conn.close()


# # ----------------------------------------------------
# # Pipeline Function
# # ----------------------------------------------------

# def process_uploaded_documents():

#     return insert_uploaded_documents()


# # ----------------------------------------------------
# # Testing
# # ----------------------------------------------------

# if __name__ == "__main__":

#     result = process_uploaded_documents()

#     if result is not None:

#         document_id, already_exists = result
  
#         print(f"\nDocument ID     : {document_id}")
#         print(f"Already Exists : {already_exists}")   


from datetime import datetime

from app.pipeline_DB.database.scripts.db_connection import get_connection
from app.pipeline_DB.database.scripts.aws_config import BUCKET_NAME


# ----------------------------------------------------
# Insert One Uploaded Document
# ----------------------------------------------------

def insert_uploaded_document(
    image_name: str,
    object_key: str
):

    conn = get_connection()
    cur = conn.cursor()

    try:

        try:

            page_number = int(
                image_name.split("_")[-1]
                .replace(".jpg", "")
                .replace(".jpeg", "")
                .replace(".png", "")
            )

        except Exception:

            page_number = 1

        upload_time = datetime.now()

        cur.execute(
            """
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
            """,
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

            conn.commit()

            print(f"✓ New Invoice Inserted : {image_name}")
            print(f"Document ID : {row[0]}")

            return row[0], False

        # Invoice already exists

        cur.execute(
            """
            SELECT document_id,
                   processing_status
            FROM uploaded_documents
            WHERE object_key=%s
            """,
            (object_key,)
        )

        existing = cur.fetchone()

        conn.commit()

        print(f"• Invoice Already Exists : {image_name}")
        print(f"Document ID : {existing[0]}")

        return existing[0], True

    except Exception as e:

        conn.rollback()
        raise e

    finally:

        cur.close()
        conn.close()


def process_uploaded_documents(
    image_name,
    object_key
):
    return insert_uploaded_document(
        image_name,
        object_key
    )