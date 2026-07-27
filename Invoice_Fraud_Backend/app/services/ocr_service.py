from paddleocr import PaddleOCR

# Initialize only once
ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en"
)

def extract_text(image_path):

    result = ocr.ocr(image_path, cls=True)

    extracted_text = []

    if result:

        for line in result[0]:

            text = line[1][0]
            confidence = line[1][1]

            extracted_text.append({
                "text": text,
                "confidence": round(confidence, 4)
            })

    return extracted_text