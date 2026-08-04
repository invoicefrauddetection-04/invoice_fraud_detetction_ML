'''from app.services.ocr_service import extract_text

image_path = "uploads/images/Invoice_1_page_1.jpg"

result = extract_text(image_path)

print("\nDetected Text\n")

for item in result:

    print(item)''' 


'''from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False
)

print("OCR Loaded Successfully!")''' 


from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False
)

result = ocr.predict("uploads/images/Invoice_1_page_1.jpg")

print(result)