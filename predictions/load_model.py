import os
import joblib

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACT_DIR = os.path.join(ROOT_DIR, "ml", "artifacts")

# Load preprocessing pipeline
preprocessor = joblib.load(
    os.path.join(ARTIFACT_DIR, "preprocessor.pkl")
)

# Load trained LightGBM model
model = joblib.load(
    os.path.join(ARTIFACT_DIR, "best_model.pkl")
)