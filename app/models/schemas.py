from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class CustomerFeatures(BaseModel):
    customer_id: Optional[str] = Field(
        default=None,
        description="Optional customer identification number",
        json_schema_extra={"example": "CUST-1001"},
    )
    tenure_months: int = Field(
        ...,
        ge=0,
        description="Customer account age in months",
        json_schema_extra={"example": 12},
    )
    monthly_charges: float = Field(
        ...,
        ge=0.0,
        description="Monthly bill amount",
        json_schema_extra={"example": 85.50},
    )
    total_charges: float = Field(
        ...,
        ge=0.0,
        description="Lifetime total charges",
        json_schema_extra={"example": 1026.00},
    )
    support_tickets: int = Field(
        ...,
        ge=0,
        description="Support tickets opened",
        json_schema_extra={"example": 5},
    )


class PredictionResponse(BaseModel):
    customer_id: Optional[str] = Field(
        default=None, json_schema_extra={"example": "CUST-1001"}
    )
    churn_prediction: int = Field(
        ..., description="0 for Stay, 1 for Churn", json_schema_extra={"example": 1}
    )
    churn_probability: float = Field(
        ...,
        description="Probability of churn (0.0 to 1.0)",
        json_schema_extra={"example": 0.8425},
    )
    risk_level: str = Field(
        ...,
        description="CRITICAL, MODERATE, or LOW",
        json_schema_extra={"example": "CRITICAL"},
    )
    retention_strategy: str = Field(
        ...,
        description="Recommended action plan",
        json_schema_extra={
            "example": "Trigger priority outbound call with strategy: Variant_A_20_Percent_Discount."
        },
    )
    ab_variant: str = Field(
        ...,
        description="Assigned experiment variant",
        json_schema_extra={"example": "Variant_A_20_Percent_Discount"},
    )


class FeatureExplanationResponse(BaseModel):
    customer_id: Optional[str]
    feature_contributions: Dict[str, float]


class BatchPredictionResponse(BaseModel):
    total_records: int
    predictions: List[PredictionResponse]
