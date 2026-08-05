from app.pipeline_DB.database.scripts.insert_uploaded_document import process_uploaded_documents
from app.pipeline_DB.database.scripts.insert_ocr_result import process_ocr
from app.pipeline_DB.predictions.feature_engineering import process_features
from app.pipeline_DB.predictions.prediction_service import process_predictions
from app.pipeline_DB.predictions.shap_service import process_shap


# ----------------------------------------------------
# End-to-End ML Pipeline
# ----------------------------------------------------

def run_pipeline():

    print("\n===================================")
    print("Pipeline Started")
    print("===================================\n")

    # Register uploaded invoice
    result = process_uploaded_documents()

    if result is None:

        print("No images found in S3.")

        return

    document_id, already_exists = result

    print(f"Document ID : {document_id}")

    # Skip duplicate invoices
    if already_exists:

        print("\n===================================")
        print("Invoice already exists.")
        print("Skipping pipeline execution.")
        print("===================================")

        return

    try:

        process_ocr(document_id)

        process_features(document_id)

        process_predictions(document_id)

        process_shap(document_id)

        print("\n===================================")
        print("Pipeline Completed Successfully")
        print("===================================")

    except Exception as e:

        print("\n===================================")
        print("Pipeline Failed")
        print("===================================")

        print(e)


# ----------------------------------------------------
# Testing Block
# ----------------------------------------------------

if __name__ == "__main__":

    run_pipeline()