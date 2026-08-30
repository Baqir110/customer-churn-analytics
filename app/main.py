import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.endpoints import router as api_router

app = FastAPI(title="Customer Churn Analytics API", version="1.0.0")

# Instrument FastAPI app and expose Prometheus /metrics endpoint
Instrumentator().instrument(app).expose(app)

# Include API routes
app.include_router(api_router, prefix="/api/v1/churn", tags=["churn"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
