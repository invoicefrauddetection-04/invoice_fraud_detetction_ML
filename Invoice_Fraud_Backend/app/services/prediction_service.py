from app.database.postgres import get_connection


def get_prediction(image_name):

    conn = get_connection()

    cur = conn.cursor()

    try:

        # -----------------------------------------
        # Get document_id using image_name
        # -----------------------------------------

        cur.execute(
            """
            SELECT document_id
            FROM uploaded_documents
            WHERE image_name = %s
            """,
            (image_name,)
        )

        document = cur.fetchone()

        if document is None:

            return {

                "status": "processing",

                "message": "Document not found in database"

            }

        document_id = document[0]

        # -----------------------------------------
        # Fetch prediction
        # -----------------------------------------

        cur.execute(
            """
            SELECT
                prediction,
                fraud_probability,
                model_name,
                prediction_timestamp
            FROM prediction_results
            WHERE document_id = %s
            """,
            (document_id,)
        )

        result = cur.fetchone()

        # -----------------------------------------
        # Prediction not generated yet
        # -----------------------------------------

        if result is None:

            return {

                "status": "processing",

                "document_id": document_id,

                "message": "Prediction is still being generated"

            }

        # -----------------------------------------
        # Prediction available
        # -----------------------------------------

        return {

            "status": "success",

            "document_id": document_id,

            "prediction": result[0],

            "fraud_probability": float(result[1]),

            "model_name": result[2],

            "prediction_timestamp": str(result[3])

        }

    finally:

        cur.close()

        conn.close()