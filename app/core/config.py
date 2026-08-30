import os


class Settings:
    PROJECT_NAME: str = "Customer Churn Analytics API"
    MODEL_PATH: str = os.getenv("MODEL_PATH", "data/churn_model.joblib")


settings = Settings()
