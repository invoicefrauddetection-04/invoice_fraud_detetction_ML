from predictions.feature_engineering import prepare_features
from predictions.load_model import model, preprocessor


def predict_invoice(document_id):
    feature_df = prepare_features(document_id)

    transformed = preprocessor.transform(feature_df)

    prediction = model.predict(transformed)[0]
    probability = model.predict_proba(transformed)[0][1]

    label = "Fraud" if prediction == 1 else "Genuine"

    return label, float(probability)


# ----------------------------------------------------
# Testing Purpose Only
# ----------------------------------------------------

if __name__ == "__main__":

    try:
        document_id = int(input("Enter Document ID: "))

        prediction, probability = predict_invoice(document_id)

        print("\nPrediction Results")
        print("------------------")
        print(f"Document ID       : {document_id}")
        print(f"Prediction        : {prediction}")
        print(f"Fraud Probability : {probability:.4f}")

    except ValueError:
        print("Invalid Document ID. Please enter a numeric value.")

    except Exception as e:
        print(f"Error: {e}")