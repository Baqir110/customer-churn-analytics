from fastapi import APIRouter, HTTPException
from app.models.schemas import CustomerFeatures, PredictionResponse
from app.ml.predict import predict_churn_risk
from app.services.strategy import get_retention_strategy

router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict_churn(features: CustomerFeatures):
    try:
        prediction, prob = predict_churn_risk(features.model_dump())
        risk, strategy = get_retention_strategy(prob)
        
        return PredictionResponse(
            churn_prediction=prediction,
            churn_probability=prob,
            risk_level=risk,
            retention_strategy=strategy
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))