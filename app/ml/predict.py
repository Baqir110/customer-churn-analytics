import os
import joblib
import pandas as pd
from app.core.config import settings

def load_model():
    if not os.path.exists(settings.MODEL_PATH):
        raise FileNotFoundError(
            f"Model binary not found at {settings.MODEL_PATH}. Run training script first."
        )
    return joblib.load(settings.MODEL_PATH)

def predict_churn_risk(features_dict: dict):
    model = load_model()
    input_df = pd.DataFrame([features_dict])
    
    prob = float(model.predict_proba(input_df)[0][1])
    prediction = int(prob >= 0.5)
    
    return prediction, round(prob, 4)