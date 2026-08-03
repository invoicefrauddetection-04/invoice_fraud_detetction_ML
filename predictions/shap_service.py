import json
import shap
import pandas as pd

from database.scripts.db_connection import get_connection

from predictions.predictor import predict_invoice

from predictions.load_model import (
    model,
    preprocessor
)

# ----------------------------------------------------
# Initialize SHAP Explainer
# ----------------------------------------------------

explainer = shap.TreeExplainer(model)

feature_names = preprocessor.get_feature_names_out()

feature_names = [

    col.replace("remainder__", "")
       .replace("onehot__", "")

    for col in feature_names

]

# ----------------------------------------------------
# Get Predicted Documents
# ----------------------------------------------------

def get_predicted_documents():

    conn = get_connection()
    cur = conn.cursor()

    query = """
       SELECT document_id
       FROM uploaded_documents
       WHERE processing_status = 'PREDICTED'
       AND upload_timestamp = (
                                SELECT MAX(upload_timestamp)
                                FROM uploaded_documents
                                WHERE processing_status = 'PREDICTED'
       );
    """

    cur.execute(query)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

# ----------------------------------------------------
# Generate SHAP
# ----------------------------------------------------

def generate_shap(feature_df):

    processed_features = preprocessor.transform(feature_df)

    if hasattr(processed_features, "toarray"):
        processed_features = processed_features.toarray()

    processed_df = pd.DataFrame(

        processed_features,

        columns=feature_names

    )

    shap_values = explainer.shap_values(processed_df)

    if isinstance(shap_values, list):
        shap_values = shap_values[0]

    explanation = shap.Explanation(

        values=shap_values[0],

        base_values=explainer.expected_value,

        data=processed_df.iloc[0],

        feature_names=processed_df.columns

    )

    return processed_df, shap_values, explanation

# ----------------------------------------------------
# Get Top SHAP Features
# ----------------------------------------------------

def get_top_features(

    processed_df,

    shap_values,

    top_n=3

):

    shap_df = pd.DataFrame({

        "feature_name":

            processed_df.columns,

        "feature_value":

            processed_df.iloc[0].values,

        "shap_value":

            shap_values[0]

    })

    shap_df["importance_score"] = (

        shap_df["shap_value"].abs()

    )

    shap_df = (

        shap_df

        .sort_values(

            "importance_score",

            ascending=False

        )

        .head(top_n)

        .reset_index(drop=True)

    )

    return shap_df

# ----------------------------------------------------
# Save SHAP Explanation
# ----------------------------------------------------

def save_shap(

    cur,

    document_id,

    prediction,

    fraud_probability,

    base_value,

    top_features

):

    query = """

        INSERT INTO shap_explanations

        (

            document_id,

            prediction,

            fraud_probability,

            base_value,

            top_features

        )

        VALUES

        (%s,%s,%s,%s,%s)

        ON CONFLICT (document_id)

        DO UPDATE SET

            prediction = EXCLUDED.prediction,

            fraud_probability = EXCLUDED.fraud_probability,

            base_value = EXCLUDED.base_value,

            top_features = EXCLUDED.top_features,

            created_at = CURRENT_TIMESTAMP;

    """

    cur.execute(

        query,

        (

            document_id,

            prediction,

            round(fraud_probability,5),

            base_value,

            json.dumps(

                top_features.to_dict(

                    orient="records"

                )

            )

        )

    )

    return {

        "document_id": document_id,

        "prediction": prediction,

        "fraud_probability": round(fraud_probability,5)

    }

# ----------------------------------------------------
# Update Processing Status
# ----------------------------------------------------

def update_processing_status(

    cur,

    document_id

):

    query = """

        UPDATE uploaded_documents

        SET processing_status='SHAP_COMPLETED'

        WHERE document_id=%s;

    """

    cur.execute(

        query,

        (document_id,)

    )

    # ----------------------------------------------------
    # Pipeline Function
    # ----------------------------------------------------

def process_shap():

    rows = get_predicted_documents()

    if not rows:

        print("No documents ready for SHAP generation.")

        return

    conn = get_connection()

    cur = conn.cursor()

    try:

        for (document_id,) in rows:

            try:

                print("\n===================================")
                print(f"Processing Document : {document_id}")
                print("===================================")

                # Prediction + Feature Data
                prediction, fraud_probability, feature_df = predict_invoice(
                    document_id
                )

                # Generate SHAP
                processed_df, shap_values, explanation = generate_shap(
                    feature_df
                )

                # Top Features
                top_features = get_top_features(

                    processed_df,

                    shap_values

                )

                # Save
                result = save_shap(

                    cur,

                    document_id,

                    prediction,

                    fraud_probability,

                    float(explanation.base_values),

                    top_features

                )

                # Update Status
                update_processing_status(

                    cur,

                    document_id

                )

                print("\n✓ SHAP Explanation Saved")

                print(result)

            except Exception as e:

                print(f"\n✗ Failed for Document {document_id}")

                print(e)

                continue

        conn.commit()

        print("\n===================================")
        print("All SHAP Explanations Generated.")
        print("===================================")

    finally:

        cur.close()

        conn.close()

