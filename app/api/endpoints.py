from fastapi import APIRouter, HTTPException

from app.core.logging import logger
from app.ml.predict import predict_churn_risk
from app.models.schemas import CustomerFeatures, PredictionResponse
from app.services.strategy import get_retention_strategy

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "customer-churn-analytics"}


@router.post("/predict", response_model=PredictionResponse)
async def predict_churn(features: CustomerFeatures):
    try:
        prediction, prob = predict_churn_risk(features.model_dump())
        risk, strategy = get_retention_strategy(prob)

        logger.info(
            f"Prediction completed - Tenure: {features.tenure_months}m | "
            f"Risk: {risk} | Prob: {prob}"
        )

        return PredictionResponse(
            churn_prediction=prediction,
            churn_probability=prob,
            risk_level=risk,
            retention_strategy=strategy,
        )
    except FileNotFoundError as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
