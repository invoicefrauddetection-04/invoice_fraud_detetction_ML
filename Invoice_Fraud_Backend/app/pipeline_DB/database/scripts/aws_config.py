# AWS Credentials
from dotenv import load_dotenv
import os

'''AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER")  '''


load_dotenv()

# Support Backend names as well as DB names

AWS_ACCESS_KEY = (
    os.getenv("AWS_ACCESS_KEY")
    or os.getenv("AWS_ACCESS_KEY_ID")
)

AWS_SECRET_KEY = (
    os.getenv("AWS_SECRET_KEY")
    or os.getenv("AWS_SECRET_ACCESS_KEY")
)

AWS_REGION = os.getenv("AWS_REGION")

BUCKET_NAME = (
    os.getenv("BUCKET_NAME")
    or os.getenv("AWS_BUCKET_NAME")
)

IMAGE_FOLDER = (
    os.getenv("IMAGE_FOLDER")
    or "converted_images/"
)

print("AWS_REGION   :", AWS_REGION)
print("BUCKET_NAME  :", BUCKET_NAME)
print("IMAGE_FOLDER :", IMAGE_FOLDER)