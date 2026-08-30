from locust import HttpUser, between, task


class ChurnApiUser(HttpUser):
    wait_time = between(0.5, 2.0)

    @task
    def predict_churn(self):
        payload = {
            "tenure_months": 6,
            "monthly_charges": 95.0,
            "total_charges": 570.0,
            "support_tickets": 4,
        }
        self.client.post("/api/v1/churn/predict", json=payload)
