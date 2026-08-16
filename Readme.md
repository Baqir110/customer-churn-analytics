# Customer Churn Analytics API

A production-grade machine learning microservice for predicting customer churn risk and prescribing automated retention strategies based on account tenure, monthly charges, and support friction metrics.

---

## 🏗️ Architecture

```text
 Customer Metrics (JSON)
          │
          ▼
   ┌──────────────┐
   │ FastAPI API  │
   └──────┬───────┘
          │
          ▼
   ┌──────────────┐
   │ Scikit-Learn │ ──► Standard Scaler + Random Forest Classifier
   │ ML Pipeline  │
   └──────┬───────┘
          │
          ▼
   ┌────────────────────────────────┐
   │ Risk Assessment & Strategy JSON│
   └────────────────────────────────┘
```

---

## ⚡ Key Features

* **Machine Learning Inference**: Serves predictions using a `scikit-learn` `Pipeline` (StandardScaler + RandomForestClassifier).
* **Automated Risk Triage**: Categorizes customers into `CRITICAL`, `MODERATE`, or `LOW` risk tiers based on probability thresholds.
* **Prescriptive Retention**: Recommends action items (discounts, surveys, engagement calls) matched to risk tier.
* **Containerized & Tested**: Docker compose setup with complete `pytest` validation suite.

---

## 🛠️ Tech Stack

* **Language**: Python 3.11
* **ML Libraries**: Scikit-Learn, Pandas, NumPy, Joblib
* **API Framework**: FastAPI, Pydantic v2
* **Containerization & Testing**: Docker, Pytest

---

## 🚀 Quickstart

1. **Install Dependencies & Train Model:**
   ```powershell
   pip install -r requirements.txt
   python -m app.ml.train
   ```

2. **Start the API:**
   ```powershell
   python -m app.main
   ```
   Interactive Swagger UI: `http://127.0.0.1:8000/docs`

3. **Run Tests:**
   ```powershell
   python -m pytest
   ```

4. **Run via Docker:**
   ```powershell
   docker compose up --build
   ```

---

## 📊 Sample Payload & Output

**POST `/api/v1/churn/predict`**

**Request:**
```json
{
  "tenure_months": 2,
  "monthly_charges": 115.0,
  "total_charges": 230.0,
  "support_tickets": 7
}
```

**Response:**
```json
{
  "churn_prediction": 1,
  "churn_probability": 0.8425,
  "risk_level": "CRITICAL",
  "retention_strategy": "Trigger priority outbound retention call and offer 20% renewal discount."
}
```
