from app.services.ocr_service import extract_text

image_path = "uploads/images/Invoice_1_page_1.jpg"

result = extract_text(image_path)

print("\nDetected Text\n")

for item in result:

    print(item)