import uvicorn
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.endpoints import router as api_router
from app.ml.drift import generate_drift_report, get_target_path

app = FastAPI(title="Customer Churn Analytics API", version="1.0.0")

# Instrument Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Include API endpoints
app.include_router(api_router, prefix="/api/v1/churn", tags=["churn"])


@app.get("/", tags=["root"])
def read_root():
    """Root endpoint providing service status and quick navigation links."""
    return {
        "status": "online",
        "service": "Customer Churn Analytics API",
        "endpoints": {
            "docs": "/docs",
            "metrics": "/metrics",
            "drift_report": "/drift",
            "api": "/api/v1/churn",
        },
    }


@app.get("/drift", response_class=FileResponse, tags=["monitoring"])
def get_drift_report(background_tasks: BackgroundTasks):
    """Serves the data drift report instantly and refreshes it in the background."""
    try:
        report_path = get_target_path()

        # Generate on first request if file does not exist
        if not report_path.exists() or report_path.stat().st_size == 0:
            report_path = generate_drift_report()
        else:
            # Refresh in background so API remains fast
            background_tasks.add_task(generate_drift_report)

        return FileResponse(path=report_path, media_type="text/html")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to serve drift report: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
