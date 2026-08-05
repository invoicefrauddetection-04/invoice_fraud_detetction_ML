import json
import shap
import pandas as pd

from app.pipeline_DB.database.scripts.db_connection import get_connection

from app.pipeline_DB.predictions.predictor import predict_invoice
from app.pipeline_DB.predictions.load_model import model, preprocessor

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

    # Compatible with LightGBM + SHAP
    if isinstance(shap_values, list):
        shap_values = shap_values[-1]

    base_value = explainer.expected_value

    if isinstance(base_value, (list, tuple)):
        base_value = base_value[-1]

    if hasattr(base_value, "__len__") and not isinstance(base_value, str):
        base_value = float(base_value[0])

    explanation = shap.Explanation(

        values=shap_values[0],

        base_values=float(base_value),

        data=processed_df.iloc[0],

        feature_names=processed_df.columns

    )

    return processed_df, shap_values, explanation


# ----------------------------------------------------
# Get Top SHAP Features
# ----------------------------------------------------

def get_top_features(processed_df, shap_values, top_n=3):

    shap_df = pd.DataFrame({

        "feature_name": processed_df.columns,

        "feature_value": processed_df.iloc[0].values,

        "shap_value": shap_values[0]

    })

    shap_df["importance_score"] = shap_df["shap_value"].abs()

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

    # Convert dataframe to object type first
    top_features = top_features.astype(object)

    # Replace NaN values with None
    top_features = top_features.where(
        pd.notnull(top_features),
        None
    )

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

            round(float(fraud_probability), 5),

            float(base_value),

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

        "fraud_probability": round(float(fraud_probability), 5)

    }


# ----------------------------------------------------
# Update Processing Status
# ----------------------------------------------------

def update_processing_status(cur, document_id):

    query = """

        UPDATE uploaded_documents

        SET processing_status='SHAP_COMPLETED'

        WHERE document_id=%s;

    """

    cur.execute(query, (document_id,))


# ----------------------------------------------------
# Pipeline Function
# ----------------------------------------------------

def process_shap(document_id):

    conn = get_connection()
    cur = conn.cursor()

    try:

        print("\n===================================")
        print(f"Processing Document : {document_id}")
        print("===================================")

        # Prediction + Features
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

        # Save SHAP
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

        conn.commit()

        print("\n✓ SHAP Explanation Saved")
        print(result)

    except Exception as e:

        conn.rollback()

        print(f"\n✗ Failed for Document {document_id}")
        print(e)

    finally:

        cur.close()
        conn.close()

'''
# ----------------------------------------------------
# Testing Block
# ----------------------------------------------------

if __name__ == "__main__":

    try:

        document_id = int(input("Enter Document ID: "))
        process_shap(document_id)

    except ValueError:

        print("Please enter a valid Document ID.")
'''