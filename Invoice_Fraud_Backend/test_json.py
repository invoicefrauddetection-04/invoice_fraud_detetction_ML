from app.services.ocr_service import extract_text
from app.services.json_service import build_invoice_json
from app.services.json_service import save_json_locally

image = "uploads/images/Invoice_1_page_1.jpg"

ocr = extract_text(image)

invoice = build_invoice_json(
    "Invoice_1.pdf",
    ocr
)

print(invoice)

path = save_json_locally(invoice)

print("JSON Saved At:")
print(path)