import pandas as pd

from datetime import datetime

from database.scripts.db_connection import get_connection

from predictions.supplier_lookup import get_supplier_features

#-----------------------------------
# Fetch OCR Data
#-----------------------------------

def get_ocr_data(document_id):
    """
    Fetch OCR extracted invoice details.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            supplier_id,
            invoice_date,
            payment_terms,
            invoice_type,
            total_amount
        FROM ocr_results
        WHERE document_id = %s;
    """

    cur.execute(query, (document_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        raise Exception(f"No OCR data found for document_id {document_id}")

    return {
        "supplier_id": row[0],
        "invoice_date": row[1],
        "payment_terms": row[2],
        "invoice_type": row[3],
        "invoice_amount": float(row[4])
    }

#-----------------------------------
# Get upload timestamp
#-----------------------------------

def get_submission_hour(document_id):
    """
    Fetch upload timestamp from uploaded_documents.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT upload_timestamp
        FROM uploaded_documents
        WHERE document_id = %s;
    """

    cur.execute(query, (document_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        raise Exception("Upload timestamp not found.")

    uploaded_timestamp = row[0]

    return uploaded_timestamp.hour

#-----------------------------------
# Compute Global Statistics
#-----------------------------------

def get_global_invoice_stats():
    """
    Compute global average and standard deviation
    from historical invoices.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            AVG(invoice_amount),
            STDDEV(invoice_amount)
        FROM training_invoices;
    """

    cur.execute(query)

    avg_amount, std_amount = cur.fetchone()

    cur.close()
    conn.close()

    return float(avg_amount), float(std_amount)

#-----------------------------------
# Build Feature Dictionary
#-----------------------------------

def generate_features(document_id):
    """
    Generate engineered ML features.
    """

    ocr_data = get_ocr_data(document_id)

    supplier_features = get_supplier_features(
        ocr_data["supplier_id"]
    )

    submission_hour = get_submission_hour(document_id)

    avg_amount, std_amount = get_global_invoice_stats()

    invoice_amount = ocr_data["invoice_amount"]

    invoice_amount_zscore = (
        (invoice_amount - avg_amount) /
        std_amount
    )

    invoice_date = ocr_data["invoice_date"]

    invoice_month = invoice_date.month

    invoice_weekday = invoice_date.weekday()

    invoice_quarter = ((invoice_month - 1) // 3) + 1

    is_weekend = 1 if invoice_weekday >= 5 else 0

    late_night_submission_flag = (
        1 if submission_hour >= 22 or submission_hour <= 5
        else 0
    )

    features = {

        "invoice_amount": invoice_amount,

        "payment_terms": ocr_data["payment_terms"],

        "invoice_type": ocr_data["invoice_type"],

        "submission_hour": submission_hour,

        # Feature expected by trained model
        "supplier_frequency":
                        supplier_features["supplier_frequency"],

        # Behavioural features
        "supplier_invoice_count_30d":
                        supplier_features["supplier_invoice_count_30d"],

        "supplier_avg_amount_90d":
                        supplier_features["supplier_avg_amount_90d"],

        "invoice_amount_zscore":
            invoice_amount_zscore,

        "late_night_submission_flag":
            late_night_submission_flag,

        "supplier_country":
            supplier_features["supplier_country"],

        "supplier_age_days":
            supplier_features["supplier_age_days"],

        "supplier_risk_score":
            supplier_features["supplier_risk_score"],

        "blacklisted_flag":
            supplier_features["blacklisted_flag"],

        "avg_invoice_amount":
            supplier_features["avg_invoice_amount"],

        "region":
            supplier_features["region"],

        "annual_budget":
            supplier_features["annual_budget"],

        "invoice_month":
            invoice_month,

        "invoice_weekday":
            invoice_weekday,

        "invoice_quarter":
            invoice_quarter,

        "is_weekend":
            is_weekend

    }

    return features


#-----------------------------------
# Convert Dictionary -> DataFrame
#-----------------------------------


def prepare_features(document_id):
    """
    Prepare model input dataframe.
    """

    features = generate_features(document_id)

    print("\nGenerated Feature Dictionary:\n")

    for key, value in features.items():
        print(f"{key:35} : {value}")

    df = pd.DataFrame([features])

    column_order = [

    "invoice_amount",

    "payment_terms",

    "invoice_type",

    "submission_hour",

    "supplier_invoice_count_30d",

    "supplier_avg_amount_90d",

    "invoice_amount_zscore",

    "late_night_submission_flag",

    "supplier_country",

    "supplier_age_days",

    "supplier_risk_score",

    "blacklisted_flag",

    "avg_invoice_amount",

    "region",

    "annual_budget",

    "invoice_month",

    "invoice_weekday",

    "invoice_quarter",

    "is_weekend",
    
    "supplier_frequency"

]

    df = df[column_order]

    print("\nFinal Model Columns:")
    print(df.columns.tolist())

    return df

#-----------------------------------
# Update Processing Status
#-----------------------------------

def update_processing_status(document_id):

    conn = get_connection()
    cur = conn.cursor()

    query = """
        UPDATE uploaded_documents
        SET processing_status='FEATURES_GENERATED'
        WHERE document_id=%s;
    """

    cur.execute(query,(document_id,))

    conn.commit()

    cur.close()
    conn.close()

'''
#-----------------------------------
# Testing Block
#-----------------------------------

if __name__ == "__main__":

    document_id = 27

    feature_df = prepare_features(document_id)

    print("\nGenerated Features\n")

    print(feature_df)

    print("\nColumns\n")

    print(feature_df.columns.tolist())

    print("\nShape\n")

    print(feature_df.shape)

'''
# ----------------------------------------------------
# Pipeline Function
# ----------------------------------------------------

def process_features(document_id):

    try:

        print("\n===================================")
        print(f"Processing Document : {document_id}")
        print("===================================")

        feature_df = prepare_features(document_id)

        print("\nGenerated Features\n")
        print(feature_df)

        update_processing_status(document_id)

        print(f"\n✓ Features generated for Document {document_id}")

    except Exception as e:

        print(f"\n✗ Failed for Document {document_id}")
        print(e)

'''
if __name__ == "__main__":

    try:
        document_id = int(input("Enter Document ID: "))
        process_features(document_id)

    except ValueError:
        print("Please enter a valid numeric Document ID.")
'''