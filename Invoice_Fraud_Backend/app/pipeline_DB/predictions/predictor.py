from app.pipeline_DB.predictions.feature_engineering import prepare_features
from app.pipeline_DB.predictions.load_model import model, preprocessor
from app.pipeline_DB.database.scripts.db_connection import get_connection


# ----------------------------------------------------
# Predict Invoice
# ----------------------------------------------------

def predict_invoice(document_id):
    """
    Generate fraud prediction for a document.

    Returns
    -------
    tuple
        (
            prediction_label,
            fraud_probability,
            feature_df
        )
    """

    # Generate engineered features
    feature_df = prepare_features(document_id)

    print("\nGenerated Columns:")
    print(feature_df.columns.tolist())

    print("\nExpected Columns:")
    print(preprocessor.feature_names_in_)
    
    # Preprocess features
    transformed_features = preprocessor.transform(feature_df)

    # Prediction
    prediction = model.predict(transformed_features)[0]

    # Fraud Probability
    probability = model.predict_proba(transformed_features)[0][1]

    # Convert prediction to label
    prediction_label = (
        "Fraud"
        if prediction == 1
        else "Genuine"
    )

    return (
        prediction_label,
        float(probability),
        feature_df
    )


# ----------------------------------------------------
# Get Feature Generated Documents
# ----------------------------------------------------

def get_feature_generated_documents():
    """
    Fetch documents whose features have been generated
    and are ready for prediction.
    """

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT document_id
        FROM uploaded_documents
        WHERE processing_status = 'FEATURES_GENERATED'
        ORDER BY document_id;
    """

    cur.execute(query)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


# ----------------------------------------------------
# Testing
# ----------------------------------------------------

if __name__ == "__main__":

    rows = get_feature_generated_documents()

    if not rows:

        print("No documents ready for prediction.")

    else:

        for (document_id,) in rows:

            try:

                prediction, probability, feature_df = predict_invoice(
                    document_id
                )

                print("\n===================================")
                print(f"Document ID       : {document_id}")
                print(f"Prediction        : {prediction}")
                print(f"Fraud Probability : {probability:.4f}")

                print("\nFeature DataFrame")
                print(feature_df)

            except Exception as e:

                print(f"\n✗ Failed for Document {document_id}")
                print(e)

                continue