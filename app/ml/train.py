import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def train_churn_model():
    np.random.seed(42)
    n_samples = 1200

    tenure = np.random.randint(1, 72, n_samples)
    monthly_charges = np.random.uniform(20.0, 120.0, n_samples)
    total_charges = tenure * monthly_charges + np.random.normal(0, 50, n_samples)
    support_tickets = np.random.poisson(2, n_samples)

    # Calculate churn probability based on tenure, price, and support friction
    logits = -2.0 - (0.04 * tenure) + (0.025 * monthly_charges) + (0.45 * support_tickets)
    churn_prob = 1 / (1 + np.exp(-logits))
    churn = (np.random.uniform(0, 1, n_samples) < churn_prob).astype(int)

    df = pd.DataFrame({
        "tenure_months": tenure,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "support_tickets": support_tickets,
        "churn": churn
    })

    X = df[["tenure_months", "monthly_charges", "total_charges", "support_tickets"]]
    y = df["churn"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X_train, y_train)

    os.makedirs("data", exist_ok=True)
    joblib.dump(pipeline, "data/churn_model.joblib")
    print("Model trained and exported to data/churn_model.joblib")

if __name__ == "__main__":
    train_churn_model()