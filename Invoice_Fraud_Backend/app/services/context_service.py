from app.database.postgres import get_connection


def get_invoice_context(document_id: int):

    conn = get_connection()
    cur = conn.cursor()

    try:

        # =====================================================
        # 1. uploaded_documents
        # =====================================================

        cur.execute(
            """
            SELECT
                document_id,
                image_name,
                upload_timestamp,
                processing_status
            FROM uploaded_documents
            WHERE document_id = %s
            """,
            (document_id,)
        )

        document = cur.fetchone()

        if document is None:

            return {
                "status": "error",
                "message": "Document not found"
            }

        document_info = {

            "document_id": document[0],
            "image_name": document[1],
            "upload_timestamp": str(document[2]),
            "processing_status": document[3]

        }

        # =====================================================
        # 2. OCR Results
        # =====================================================

        cur.execute(
            """
            SELECT

                supplier_id,
                invoice_id,
                invoice_date,
                payment_terms,
                invoice_type,
                supplier_country,
                total_amount

            FROM ocr_results

            WHERE document_id = %s
            """,
            (document_id,)
        )

        row = cur.fetchone()

        invoice_info = {}

        if row:

            invoice_info = {

                "supplier_id": row[0],
                "invoice_id": row[1],
                "invoice_date": str(row[2]),
                "payment_terms": row[3],
                "invoice_type": row[4],
                "supplier_country": row[5],
                "total_amount": float(row[6])

            }

        # =====================================================
        # 3. Prediction
        # =====================================================

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

        row = cur.fetchone()

        prediction_info = {}

        if row:

            prediction_info = {

                "prediction": row[0],
                "fraud_probability": float(row[1]),
                "model_name": row[2],
                "prediction_timestamp": str(row[3])

            }

        # =====================================================
        # 4. SHAP
        # =====================================================

        cur.execute(
            """
            SELECT

                prediction,
                fraud_probability,
                base_value,
                top_features,
                created_at

            FROM shap_explanations

            WHERE document_id = %s
            """,
            (document_id,)
        )

        row = cur.fetchone()

        shap_ready = False
        shap_info = {}

        if row:

            shap_ready = True

            shap_info = {

                "prediction": row[0],
                "fraud_probability": float(row[1]),
                "base_value": row[2],
                "top_features": row[3],
                "created_at": str(row[4])

            }

        # =====================================================
        # Final Context
        # =====================================================
        return {

            "status": "success",

            "context_version": 1,

            "document_id": document_id,

            "prediction_ready": prediction_info is not None,

            "shap_ready": shap_ready,

            "document": document_info if document_info else {},

            "invoice": invoice_info if invoice_info else {},

            "prediction": prediction_info if prediction_info else {},

            "shap": shap_info

        }

    finally:

        cur.close()
        conn.close()
