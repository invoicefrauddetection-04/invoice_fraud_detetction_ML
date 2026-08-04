import re
from statistics import mean
from datetime import datetime


# ---------------------------------------------------------
# Generic Regex Extractor
# ---------------------------------------------------------

def extract_first(patterns, text):
    """
    Try multiple regex patterns.
    Return the first successful match.
    """

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None


# ---------------------------------------------------------
# Clean Monetary Amount
# ---------------------------------------------------------

def clean_amount(value):

    if value is None:
        return None

    value = str(value)

    value = value.replace(",", "")

    value = value.replace("₹", "")
    value = value.replace("$", "")
    value = value.replace("€", "")
    value = value.replace("£", "")

    value = value.replace("INR", "")
    value = value.replace("USD", "")
    value = value.replace("EUR", "")
    value = value.replace("GBP", "")

    value = value.strip()

    # Keep only digits and decimal point
    value = re.sub(r"[^0-9.]", "", value)

    try:
        return float(value)

    except:
        return None

# ---------------------------------------------------------
# Clean Date
# ---------------------------------------------------------

def clean_date(date_string):

    if date_string is None:
        return None

    date_string = date_string.strip()

    formats = [

        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d %b %Y",
        "%d %B %Y",
        "%Y/%m/%d"

    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                date_string,
                fmt
            ).date()

        except:

            continue

    return date_string

# ---------------------------------------------------------
# Main Parser
# ---------------------------------------------------------

def parse_ocr_json(ocr_json):

    # -----------------------------
    # Read first page
    # -----------------------------

    page = ocr_json["pages"][0]

    image_name = page.get("image_name", "")

    ocr_lines = page.get("ocr", [])

    # -----------------------------
    # Merge OCR text
    # -----------------------------

    raw_text = "\n".join(

        item.get("text", "")

        for item in ocr_lines

    )

    # -----------------------------
    # Average OCR Confidence
    # -----------------------------

    if len(ocr_lines) > 0:

        average_confidence = round(

            mean(

                item.get("confidence", 0)

                for item in ocr_lines

            ),

            4

        )

    else:

        average_confidence = 0.0

    # -----------------------------
    # Invoice Dictionary
    # -----------------------------

    invoice = {

        "image_name": image_name,

        "supplier_id": None,

        "invoice_id": None,

        "invoice_date": None,

        "payment_terms": None,

        "invoice_type": None,

        "supplier_country": None,

        "subtotal": None,

        "tax_amount": None,

        "total_amount": None,

        "currency": None,

        "raw_text": raw_text,

        "average_confidence": average_confidence

    }

    # ---------------------------------------------------------
    # Supplier ID
    # ---------------------------------------------------------

    invoice["supplier_id"] = extract_first(

    [

        r"Supplier\s*ID\s*[:#-]?\s*([A-Za-z0-9 _\-/]+)",

        r"Vendor\s*ID\s*[:#-]?\s*([A-Za-z0-9 _\-/]+)",

        r"Supplier\s*Code\s*[:#-]?\s*([A-Za-z0-9 _\-/]+)",

        r"Vendor\s*Code\s*[:#-]?\s*([A-Za-z0-9 _\-/]+)",

        r"Supplier\s*[:#-]?\s*([A-Za-z0-9 _\-/]+)"

    ],

    raw_text

)

    #print("\n========== DEBUG ==========")
    #print("Supplier ID extracted:", repr(invoice["supplier_id"]))


    # ---------------------------------------------------------
    # Invoice Number
    # ---------------------------------------------------------

    invoice["invoice_id"] = extract_first(

        [

            r"Invoice\s*No\.?\s*[:#-]?\s*([A-Za-z0-9_\-/]+)",

            r"Invoice\s*Number\s*[:#-]?\s*([A-Za-z0-9_\-/]+)",

            r"Invoice\s*ID\s*[:#-]?\s*([A-Za-z0-9_\-/]+)",

            r"Invoice\s*#\s*([A-Za-z0-9_\-/]+)",

            r"Inv\s*No\.?\s*[:#-]?\s*([A-Za-z0-9_\-/]+)",

            r"Bill\s*No\.?\s*[:#-]?\s*([A-Za-z0-9_\-/]+)"

        ],

        raw_text

    )


    # ---------------------------------------------------------
    # Invoice Date
    # ---------------------------------------------------------

    invoice_date = extract_first(

        [

            r"Invoice\s*Date\s*[:#-]?\s*([^\n]+)",

            r"Bill\s*Date\s*[:#-]?\s*([^\n]+)",

            r"Date\s*[:#-]?\s*([^\n]+)"

        ],

        raw_text

    )

    invoice["invoice_date"] = clean_date(invoice_date)


    # ---------------------------------------------------------
    # Payment Terms
    # ---------------------------------------------------------

    payment = extract_first(

        [

            r"Payment\s*Terms\s*[:#-]?\s*(NET\d+)",

            r"Terms\s*[:#-]?\s*(NET\d+)",

            r"\b(NET30)\b",

            r"\b(NET45)\b",

            r"\b(NET60)\b",

            r"\b(NET90)\b"

        ],

        raw_text

    )

    if payment:

        invoice["payment_terms"] = payment.upper()


    # ---------------------------------------------------------
    # Invoice Type
    # ---------------------------------------------------------

    invoice_type = extract_first(

        [

            r"Invoice\s*Type\s*[:#-]?\s*(GOODS|SERVICES)",

            r"Type\s*[:#-]?\s*(GOODS|SERVICES)",

            r"\b(GOODS)\b",

            r"\b(SERVICES)\b"

        ],

        raw_text

    )

    if invoice_type:

        invoice["invoice_type"] = invoice_type.upper()


    # ---------------------------------------------------------
    # Supplier Country
    # ---------------------------------------------------------

    invoice["supplier_country"] = extract_first(

        [

            r"Country\s*[:#-]?\s*([A-Za-z ]+)",

            r"Supplier\s*Country\s*[:#-]?\s*([A-Za-z ]+)",

            r"Location\s*[:#-]?\s*([A-Za-z ]+)"

        ],

        raw_text

    )

    # ---------------------------------------------------------
    # Currency
    # ---------------------------------------------------------

    currency = extract_first(

        [

            r"Currency\s*[:#-]?\s*([A-Z]{3})",

            r"\b(INR|USD|EUR|GBP|AED|CAD|AUD|JPY)\b"

        ],

        raw_text

    )

    if currency:

        invoice["currency"] = currency.upper()


    # ---------------------------------------------------------
    # Subtotal
    # ---------------------------------------------------------

    subtotal = extract_first(

        [

            r"Subtotal\s*[:#-]?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

            r"Sub\s*Total\s*[:#-]?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)"

        ],

        raw_text

    )

    invoice["subtotal"] = clean_amount(subtotal)


    # ---------------------------------------------------------
    # Tax
    # ---------------------------------------------------------

    tax = extract_first(

        [

            r"GST\s*[:#-]?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

            r"VAT\s*[:#-]?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

            r"CGST\s*[:#-]?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

            r"SGST\s*[:#-]?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

            r"IGST\s*[:#-]?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

            r"Tax\s*[:#-]?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)"

        ],

        raw_text

    )

    invoice["tax_amount"] = clean_amount(tax)


# ---------------------------------------------------------
# Total Amount
# ---------------------------------------------------------

    total = extract_first(

    [

        # Grand Total
        r"Grand\s*Total\s*[:#-]?\s*\n?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

        # Invoice Total
        r"Invoice\s*Total\s*[:#-]?\s*\n?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

        # Amount Due
        r"Amount\s*Due\s*[:#-]?\s*\n?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

        # Balance Due
        r"Balance\s*Due\s*[:#-]?\s*\n?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

        # Total Due
        r"Total\s*Due\s*[:#-]?\s*\n?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

        # Net Amount
        r"Net\s*Amount\s*[:#-]?\s*\n?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

        # Payable Amount
        r"Payable\s*Amount\s*[:#-]?\s*\n?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

        # Final Total
        r"Final\s*Total\s*[:#-]?\s*\n?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)",

        # Generic Total (KEEP LAST)
        r"\bTotal\s*:\s*\n?\s*[₹$€£]?\s*([\d,]+(?:\.\d{1,2})?)"

    ],

    raw_text

)

    invoice["total_amount"] = clean_amount(total)

    # ---------------------------------------------------------
    # Intelligent Fallbacks
    # ---------------------------------------------------------

    # If Total not found, use subtotal + tax

    if invoice["total_amount"] is None:

        if (
            invoice["subtotal"] is not None and
            invoice["tax_amount"] is not None
        ):

            invoice["total_amount"] = round(

                invoice["subtotal"] +
                invoice["tax_amount"],

                2

            )

    # If Tax missing but Total & Subtotal exist

    if (
        invoice["tax_amount"] is None and
        invoice["subtotal"] is not None and
        invoice["total_amount"] is not None
    ):

        invoice["tax_amount"] = round(

            invoice["total_amount"] -
            invoice["subtotal"],

            2

        )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    mandatory_fields = [

        "supplier_id",

        "invoice_id",

        "invoice_date",

        "total_amount"

    ]

    print("\n========== OCR Extraction ==========\n")

    for field in invoice:

        print(f"{field:20} : {invoice[field]}")

    print()

    for field in mandatory_fields:

        if invoice[field] is None:

            print(
                f"[WARNING] {field} could not be extracted."
            )

    # ---------------------------------------------------------
    # Return Parsed Invoice
    # ---------------------------------------------------------

    return invoice