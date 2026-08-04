'''from paddleocr import PaddleOCR

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

    return extracted_text''' 


'''from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False
)

def extract_text(image_path):

    results = ocr.predict(image_path)

    extracted_text = []

    for page in results:

        for text, score in zip(
                page["rec_texts"],
                page["rec_scores"]):

            extracted_text.append({
                "text": text,
                "confidence": round(float(score), 4)
            })

    return extracted_text''' 

from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False
)


def extract_text(image_path):

    results = ocr.predict(image_path)

    extracted_text = []

    if results:

        page = results[0]

        texts = page["rec_texts"]
        scores = page["rec_scores"]

        for text, score in zip(texts, scores):
            extracted_text.append({
                "text": text,
                "confidence": round(float(score), 4)
            })

    return extracted_text