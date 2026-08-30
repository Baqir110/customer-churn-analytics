import requests
import streamlit as st

st.set_page_config(
    page_title="Customer Churn Risk Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Customer Churn Risk Triage & Retention")
st.markdown(
    "Adjust customer profile parameters to compute real-time risk scores and automated retention strategies."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Profile")
    tenure_months = st.slider("Tenure (Months)", min_value=0, max_value=72, value=12)
    monthly_charges = st.slider(
        "Monthly Charges ($)", min_value=15.0, max_value=150.0, value=75.0
    )

with col2:
    st.subheader("Account Activity")
    total_charges = st.number_input(
        "Total Charges ($)", min_value=0.0, value=float(tenure_months * monthly_charges)
    )
    support_tickets = st.slider(
        "Support Tickets Opened", min_value=0, max_value=15, value=3
    )

API_URL = "http://127.0.0.1:8000/api/v1/churn/predict"

if st.button("Calculate Churn Risk", type="primary"):
    payload = {
        "tenure_months": tenure_months,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges,
        "support_tickets": support_tickets,
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            res = response.json()
            st.divider()

            risk = res["risk_level"]
            prob = res["churn_probability"]

            m1, m2 = st.columns(2)
            m1.metric("Churn Probability", f"{prob * 100:.1f}%")
            m2.metric("Risk Assessment", risk)

            if risk == "CRITICAL":
                st.error(f"**Action Required**: {res['retention_strategy']}")
            elif risk == "MODERATE":
                st.warning(f"**Recommended Action**: {res['retention_strategy']}")
            else:
                st.success(f"**Standard Lifecycle**: {res['retention_strategy']}")
        else:
            st.error("API returned an error processing the prediction.")
    except Exception as e:
        st.error(
            f"Could not connect to FastAPI endpoint at {API_URL}. Ensure the API is running."
        )
