import boto3

from database.scripts.aws_config import (
    AWS_ACCESS_KEY,
    AWS_SECRET_KEY,
    AWS_REGION,
    BUCKET_NAME,
    IMAGE_FOLDER
)


def get_s3_client():
    """
    Create and return an AWS S3 client.
    """

    return boto3.client(
        service_name="s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION
    )


def list_all_images():

    s3 = get_s3_client()

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix=IMAGE_FOLDER
    )

    if "Contents" not in response:
        return []

    return response["Contents"]