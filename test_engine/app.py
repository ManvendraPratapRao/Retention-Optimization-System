import streamlit as st
from config import RetentionConfig
from decision_engine import compute_customer_value

st.set_page_config(page_title="Retention Value Calculator", layout="wide")

st.title("📊 Customer Retention Value (MVP)")

# ---------- SIDEBAR : BUSINESS STRATEGY ----------
st.sidebar.header("⚙️ Business Strategy Settings")

avg_lifetime = st.sidebar.slider(
    "Average Customer Lifetime (months)",
    min_value=6, max_value=60, value=24
)

floor_months = st.sidebar.slider(
    "Minimum Remaining Months",
    min_value=1, max_value=12, value=3
)

margin_pct = st.sidebar.slider(
    "Profit Margin %",
    min_value=5, max_value=80, value=30
) / 100  # convert to decimal

config = RetentionConfig(avg_lifetime, floor_months, margin_pct)

# ---------- CUSTOMER INPUT ----------
st.header("Customer Information")

col1, col2 = st.columns(2)

with col1:
    tenure = st.number_input("Tenure (months)", min_value=0, max_value=120, value=6)
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=70.0)

with col2:
    contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
    partner = st.selectbox("Partner", ["Yes", "No"])

user_data = {
    "tenure": tenure,
    "MonthlyCharges": monthly_charges,
    "Contract": contract,
    "InternetService": internet,
    "Partner": partner
}

# ---------- EVALUATION ----------
if st.button("Evaluate Customer"):

    result = compute_customer_value(user_data, config)

    st.subheader("📈 Results")

    colA, colB = st.columns(2)

    colA.metric("Monthly Profit", f"${result['monthly_margin']}")
    colB.metric("Future Value At Risk", f"${result['brv']}")