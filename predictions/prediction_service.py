from datetime import datetime

from database.scripts.db_connection import get_connection

from predictions.predictor import predict_invoice


def save_prediction(document_id):
    """
    Predict invoice fraud and store prediction in database.
    """

    prediction, probability = predict_invoice(document_id)

    conn = get_connection()
    cur = conn.cursor()

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

        DO UPDATE

        SET

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

            "XGBoost",

            datetime.now()

        )

    )

    conn.commit()

    cur.close()
    conn.close()

    return {

        "document_id": document_id,

        "prediction": prediction,

        "fraud_probability": round(probability, 4),

        "model_name": "XGBoost"

    }

#----------------------------------------------------------
# Testing only
#----------------------------------------------------------

if __name__ == "__main__":

    result = save_prediction(8)

    print(result)