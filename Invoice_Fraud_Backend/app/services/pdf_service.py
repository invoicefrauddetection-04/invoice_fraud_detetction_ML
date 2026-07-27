import os
from pdf2image import convert_from_path


POPPLER_PATH = r"C:\poppler\poppler-26.02.0\Library\bin"


UPLOAD_PDF_FOLDER = "uploads/pdfs"
UPLOAD_IMAGE_FOLDER = "uploads/images"


def convert_pdf_to_images(pdf_path):

    images = convert_from_path(
        pdf_path,
        dpi=300,
        poppler_path=POPPLER_PATH
    )

    image_paths = []

    pdf_name = os.path.splitext(
        os.path.basename(pdf_path)
    )[0]

    for index, image in enumerate(images):

        image_name = f"{pdf_name}_page_{index+1}.jpg"

        save_path = os.path.join(
            UPLOAD_IMAGE_FOLDER,
            image_name
        )

        image.save(
            save_path,
            "JPEG"
        )

        image_paths.append(save_path)

    return image_paths