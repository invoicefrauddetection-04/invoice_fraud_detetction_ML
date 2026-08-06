'''from app.pipeline_DB.database.scripts.insert_uploaded_document import process_uploaded_documents
from app.pipeline_DB.database.scripts.insert_ocr_result import process_ocr
from app.pipeline_DB.predictions.feature_engineering import process_features
from app.pipeline_DB.predictions.prediction_service import process_predictions
from app.pipeline_DB.predictions.shap_service import process_shap


# ----------------------------------------------------
# End-to-End ML Pipeline
# ----------------------------------------------------

def run_pipeline(document_id):

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

    run_pipeline()'''


from app.pipeline_DB.database.scripts.insert_ocr_result import process_ocr
from app.pipeline_DB.predictions.feature_engineering import process_features
from app.pipeline_DB.predictions.prediction_service import process_predictions
from app.pipeline_DB.predictions.shap_service import process_shap


# ----------------------------------------------------
# End-to-End ML Pipeline
# ----------------------------------------------------

# def run_pipeline(document_id , already_exists):

#     print("\n===================================")
#     print("Pipeline Started")
#     print("===================================")

#     print(f"Document ID : {document_id}")

#     try:

#         print("\n========== STEP 1 ==========")
#         print("Running OCR...")
#         process_ocr(document_id)
#         print("OCR Completed")

#         print("\n========== STEP 2 ==========")
#         print("Generating Features...")
#         process_features(document_id)
#         print("Feature Engineering Completed")

#         print("\n========== STEP 3 ==========")
#         print("Running Prediction...")
#         process_predictions(document_id)
#         print("Prediction Completed")

#         print("\n========== STEP 4 ==========")
#         print("Generating SHAP...")
#         process_shap(document_id)
#         print("SHAP Completed")

#         print("\n===================================")
#         print("Pipeline Completed Successfully")
#         print("===================================")

#     except Exception as e:

#         print("\n===================================")
#         print("Pipeline Failed")
#         print("===================================")

#         import traceback
#         traceback.print_exc()

#         raise


# # ----------------------------------------------------
# # Testing
# # ----------------------------------------------------

# if __name__ == "__main__":

#     run_pipeline(1) 


def run_pipeline(document_id: int, already_exists: bool):

    print("\n===================================")
    print("Pipeline Started")
    print("===================================\n")

    print(f"Document ID : {document_id}")

    if already_exists:

        print("Invoice already exists.")
        return

    try:

        process_ocr(document_id)

        process_features(document_id)

        process_predictions(document_id)

        process_shap(document_id)

        print("Pipeline Completed Successfully")

    except Exception as e:

        print(e)