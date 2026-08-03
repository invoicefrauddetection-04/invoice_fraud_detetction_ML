import os
import re

def get_json_object_key(image_name):
    """
    Converts image filename to OCR JSON object key.

    Examples:
    Invoice_034.png      -> ocr_json/Invoice_034.json
    Invoice_3_page_1.jpg -> ocr_json/Invoice_3.json
    Invoice_3_page_2.jpg -> ocr_json/Invoice_3.json
    """

    # Remove file extension
    base_name = os.path.splitext(image_name)[0]

    # Remove '_page_<number>' suffix if present
    base_name = re.sub(r"_page_\d+$", "", base_name)

    return f"ocr_json/{base_name}.json"