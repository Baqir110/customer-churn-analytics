from pydantic import BaseModel, Field

class CustomerFeatures(BaseModel):
    tenure_months: int = Field(..., ge=0, description="Customer account age in months", example=12)
    monthly_charges: float = Field(..., ge=0.0, description="Monthly bill amount", example=85.50)
    total_charges: float = Field(..., ge=0.0, description="Lifetime total charges", example=1026.00)
    support_tickets: int = Field(..., ge=0, description="Support tickets opened", example=5)

class PredictionResponse(BaseModel):
    churn_prediction: int
    churn_probability: float
    risk_level: str
    retention_strategy: str