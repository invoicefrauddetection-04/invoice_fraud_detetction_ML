from database.scripts.insert_uploaded_document import process_uploaded_documents
from database.scripts.insert_ocr_result import process_ocr
from predictions.feature_engineering import process_features
from predictions.prediction_service import process_predictions
from predictions.shap_service import process_shap


# ----------------------------------------------------
# End-to-End ML Pipeline
# ----------------------------------------------------

def run_pipeline():

    print("\n===================================")
    print("Pipeline Started")
    print("===================================\n")

    # Register newly uploaded document
    document_id = process_uploaded_documents()

    if document_id is None:

        print("No new documents found.")

        return

    print(f"Document ID : {document_id}")

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

'''
# ----------------------------------------------------
# Testing Block
# ----------------------------------------------------

if __name__ == "__main__":

    run_pipeline()
'''