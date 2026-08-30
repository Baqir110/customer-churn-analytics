import os

import joblib
import pandas as pd

from app.core.config import settings


class ModelWrapper:
    def __init__(self):
        self._model = None

    @property
    def model(self):
        if self._model is None:
            if not os.path.exists(settings.MODEL_PATH):
                raise FileNotFoundError(
                    f"Model binary not found at {settings.MODEL_PATH}. Run training script first."
                )
            self._model = joblib.load(settings.MODEL_PATH)
        return self._model

    def predict_proba(self, df: pd.DataFrame):
        return self.model.predict_proba(df)

    def predict(self, df: pd.DataFrame):
        return self.model.predict(df)


# Global instance imported by endpoints.py and explain.py
model_wrapper = ModelWrapper()


def load_model():
    return model_wrapper.model


def predict_churn_risk(features_dict: dict):
    input_df = pd.DataFrame([features_dict])

    prob = float(model_wrapper.predict_proba(input_df)[0][1])
    prediction = int(prob >= 0.5)

    return prediction, round(prob, 4)
