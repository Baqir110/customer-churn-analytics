import os
import joblib
import pandas as pd
from fastapi import APIRouter, HTTPException
from app.models.schemas import CustomerFeatures, PredictionResponse

router = APIRouter()
MODEL_PATH = "data/churn_model.joblib"


@router.post("/predict", response_model=PredictionResponse)
async def predict_churn(features: CustomerFeatures):
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(
            status_code=500, detail="Model binary not found. Run training script first."
        )

    model = joblib.load(MODEL_PATH)

    input_df = pd.DataFrame(
        [
            {
                "tenure_months": features.tenure_months,
                "monthly_charges": features.monthly_charges,
                "total_charges": features.total_charges,
                "support_tickets": features.support_tickets,
            }
        ]
    )

    prob = float(model.predict_proba(input_df)[0][1])
    prediction = int(prob >= 0.5)

    if prob >= 0.70:
        risk = "CRITICAL"
        strategy = (
            "Trigger priority outbound retention call and offer 20% renewal discount."
        )
    elif prob >= 0.40:
        risk = "MODERATE"
        strategy = (
            "Send proactive service check-in survey and targeted onboarding tutorial."
        )
    else:
        risk = "LOW"
        strategy = "Maintain standard automated customer engagement lifecycle."

    return PredictionResponse(
        churn_prediction=prediction,
        churn_probability=round(prob, 4),
        risk_level=risk,
        retention_strategy=strategy,
    )
