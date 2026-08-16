from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI(
    title="Customer Churn Analytics API",
    version="1.0.0",
    description="Machine learning prediction service for evaluating customer churn risk and prescribing retention actions."
)

app.include_router(api_router, prefix="/api/v1/churn", tags=["Churn Analytics"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)