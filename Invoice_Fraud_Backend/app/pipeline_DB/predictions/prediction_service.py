from datetime import datetime

from app.pipeline_DB.database.scripts.db_connection import get_connection

from app.pipeline_DB.predictions.predictor import predict_invoice


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

    model_name = "LightGBM"

    cur.execute(
        query,
        (
            document_id,
            prediction,
            probability,
            model_name,
            datetime.now()
        )
    )

    return {

        "document_id": document_id,

        "prediction": prediction,

        "fraud_probability": round(probability, 4),

        "model_name": model_name,

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

def process_predictions(document_id):

    conn = get_connection()
    cur = conn.cursor()

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

        conn.commit()

        print("\nPrediction Saved Successfully")
        print(result)

    except Exception as e:

        conn.rollback()

        print(f"\n✗ Failed for Document {document_id}")
        print(e)

    finally:

        cur.close()
        conn.close()

'''
# ----------------------------------------------------------
# Testing Block
# ----------------------------------------------------------

if __name__ == "__main__":

    try:

        document_id = int(input("Enter Document ID: "))
        process_predictions(document_id)

    except ValueError:

        print("Please enter a valid Document ID.")
'''