import streamlit as st
import pandas as pd
from components.api_client import predict_single


def render_single_mode(business_config):

    st.subheader("Single Customer Prediction")

    with st.form("single_form"):

        tenure = st.number_input("Tenure (months)", 0, 120, 5)
        monthly_charges = st.number_input("Monthly Charges", 0.0, 500.0, 75.0)

        SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
        Partner = st.selectbox("Partner", ["Yes", "No"])
        Dependents = st.selectbox("Dependents", ["Yes", "No"])
        Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        PaymentMethod = st.selectbox("Payment Method",
                                     ["Electronic check", "Mailed check",
                                      "Bank transfer (automatic)", "Credit card (automatic)"])
        PaperlessBilling = st.selectbox("Paperless Billing", ["Yes", "No"])
        InternetService = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        TechSupport = st.selectbox("Tech Support", ["Yes", "No"])
        OnlineSecurity = st.selectbox("Online Security", ["Yes", "No"])
        OnlineBackup = st.selectbox("Online Backup", ["Yes", "No"])
        DeviceProtection = st.selectbox("Device Protection", ["Yes", "No"])
        StreamingTV = st.selectbox("Streaming TV", ["Yes", "No"])
        StreamingMovies = st.selectbox("Streaming Movies", ["Yes", "No"])
        include_explanation = st.checkbox("Include Explanation (SHAP)")

        submitted = st.form_submit_button("Predict")

    if submitted:

        payload = {
            "customer": {
                "tenure": tenure,
                "MonthlyCharges": monthly_charges,
                "SeniorCitizen": SeniorCitizen,
                "Partner": Partner,
                "Dependents": Dependents,
                "Contract": Contract,
                "PaymentMethod": PaymentMethod,
                "PaperlessBilling": PaperlessBilling,
                "InternetService": InternetService,
                "TechSupport": TechSupport,
                "OnlineSecurity": OnlineSecurity,
                "OnlineBackup": OnlineBackup,
                "DeviceProtection": DeviceProtection,
                "StreamingTV": StreamingTV,
                "StreamingMovies": StreamingMovies
            },
            "business_config": business_config,
            "include_explanation": include_explanation
        }

        response = predict_single(payload)

        if response.status_code == 200:
            result = response.json()
        
            st.subheader("Prediction Summary")
        
            col1, col2 = st.columns(2)
        
            col1.metric("Churn Probability", result["prediction"]["p_churn"])
            col1.metric("Segment", result["prediction"]["segment"])
            col1.metric("Decision", result["business_metrics"]["decision"])
        
            col2.metric("BRV", result["business_metrics"]["BRV"])
            col2.metric("Monthly Margin", result["business_metrics"]["monthly_margin"])
            col2.metric("Expected Gain", result["business_metrics"]["expected_gain"])
            col2.metric("ROI", result["business_metrics"]["ROI"])
        
            if result["explanation"] is not None:
                st.subheader("Top Risk Drivers")
                for feature in result["explanation"]["top_features"]:
                    st.write(f"{feature['feature']} → {feature['impact']}")
        
        else:
            st.error(response.json()["detail"])