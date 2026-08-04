from datetime import datetime

from database.scripts.db_connection import get_connection

from predictions.predictor import (
    predict_invoice,
    get_feature_generated_documents
)


# ----------------------------------------------------------
# Save Prediction
# ----------------------------------------------------------

def save_prediction(cur, document_id):
    """
    Predict invoice fraud and store prediction.
    """

    prediction, probability, feature_df = predict_invoice(document_id)

    query = """
        INSERT INTO prediction_results
        (
            document_id,
            prediction,
            fraud_probability,
            model_name,
            prediction_timestamp
        )
        VALUES
        (%s,%s,%s,%s,%s)

        ON CONFLICT (document_id)

        DO UPDATE SET

            prediction = EXCLUDED.prediction,

            fraud_probability = EXCLUDED.fraud_probability,

            model_name = EXCLUDED.model_name,

            prediction_timestamp = EXCLUDED.prediction_timestamp;
    """

    cur.execute(

        query,

        (

            document_id,

            prediction,

            probability,

            "LightGBM",

            datetime.now()

        )

    )

    return {

    "document_id": document_id,

    "prediction": prediction,

    "fraud_probability": round(probability,4),

    "model_name": "XGBoost",

    "feature_df": feature_df

}


# ----------------------------------------------------------
# Update Processing Status
# ----------------------------------------------------------

def update_processing_status(cur, document_id):

    query = """
        UPDATE uploaded_documents
        SET processing_status = 'PREDICTED'
        WHERE document_id = %s;
    """

    cur.execute(query, (document_id,))


# ----------------------------------------------------------
# Pipeline Function
# ----------------------------------------------------------

def process_predictions():

    rows = get_feature_generated_documents()

    if not rows:

        print("No documents ready for prediction.")

        return

    conn = get_connection()
    cur = conn.cursor()

    try:

        for (document_id,) in rows:

            try:

                print("\n===================================")
                print(f"Processing Document : {document_id}")
                print("===================================")

                result = save_prediction(
                    cur,
                    document_id
                )

                update_processing_status(
                    cur,
                    document_id
                )

                print("\nPrediction Saved Successfully")
                print(result)

            except Exception as e:

                print(f"\n✗ Failed for Document {document_id}")
                print(e)

                continue

        conn.commit()

        print("\n===================================")
        print("All predictions completed.")
        print("===================================")

    finally:

        cur.close()
        conn.close()


if __name__ == "__main__":

    process_predictions()