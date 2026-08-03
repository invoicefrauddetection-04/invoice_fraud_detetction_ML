import os
import joblib
from xgboost import XGBClassifier

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTIFACT_DIR = os.path.join(ROOT_DIR, "ml", "artifacts")

preprocessor = joblib.load(
    os.path.join(ARTIFACT_DIR, "preprocessor.pkl")
)

model = XGBClassifier()
model.load_model(
    os.path.join(ARTIFACT_DIR, "best_xgboost_model.json")
)