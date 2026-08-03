from database.scripts.insert_uploaded_document import process_uploaded_documents
from database.scripts.insert_ocr_result import process_ocr
from predictions.feature_engineering import process_features
from predictions.prediction_service import process_predictions
from predictions.shap_service import process_shap


def run_pipeline():

    print("\n===================================")
    print("Pipeline Started")
    print("===================================\n")

    process_uploaded_documents()

    process_ocr()

    process_features()

    process_predictions()

    process_shap()          

    print("\n===================================")
    print("Pipeline Finished")
    print("===================================")


if __name__ == "__main__":
    run_pipeline()