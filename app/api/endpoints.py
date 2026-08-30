from typing import List

import pandas as pd
from fastapi import APIRouter, HTTPException

from app.core.logging import logger
from app.ml.explain import get_feature_explanations
from app.ml.predict import model_wrapper, predict_churn_risk
from app.models.schemas import (
    BatchPredictionResponse,
    CustomerFeatures,
    FeatureExplanationResponse,
    PredictionResponse,
)
from app.services.strategy import get_retention_strategy

router = APIRouter()


def process_single_prediction(
    features: CustomerFeatures,
) -> PredictionResponse:
    payload_dict = features.model_dump(exclude={"customer_id"})
    prediction, prob = predict_churn_risk(payload_dict)
    risk, strategy, ab_variant = get_retention_strategy(prob, features.customer_id)

    return PredictionResponse(
        customer_id=features.customer_id,
        churn_prediction=prediction,
        churn_probability=prob,
        risk_level=risk,
        retention_strategy=strategy,
        ab_variant=ab_variant,
    )


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "customer-churn-analytics"}


@router.post("/predict", response_model=PredictionResponse)
async def predict_churn(features: CustomerFeatures):
    try:
        response = process_single_prediction(features)
        logger.info(
            f"Prediction completed - ID: {features.customer_id} | "
            f"Risk: {response.risk_level} | Prob: {response.churn_probability}"
        )
        return response
    except FileNotFoundError as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_churn_batch(features_list: List[CustomerFeatures]):
    if not features_list:
        raise HTTPException(
            status_code=400, detail="Batch request payload cannot be empty."
        )

    try:
        results = [process_single_prediction(item) for item in features_list]
        return BatchPredictionResponse(total_records=len(results), predictions=results)
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain", response_model=FeatureExplanationResponse)
async def explain_churn_features(features: CustomerFeatures):
    try:
        payload_dict = features.model_dump(exclude={"customer_id"})
        input_df = pd.DataFrame([payload_dict])
        contributions = get_feature_explanations(model_wrapper.model, input_df)

        return FeatureExplanationResponse(
            customer_id=features.customer_id,
            feature_contributions=contributions,
        )
    except Exception as e:
        logger.error(f"Explanation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
