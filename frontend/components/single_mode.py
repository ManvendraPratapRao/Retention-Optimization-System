import streamlit as st
import pandas as pd
import plotly.express as px
from components.api_client import predict_single


def render_single_mode(business_config):

    st.subheader("👤 Customer Profile Builder")
    st.markdown("Populate the customer details below to assess churn risk and economic impact.")

    with st.form("single_form"):
        
        tab1, tab2, tab3 = st.tabs(["📋 Demographics", "📡 Services", "📄 Contract"])
        
        with tab1:
            col_a, col_b = st.columns(2)
            gender = col_a.selectbox("Gender", ["Female", "Male"])
            SeniorCitizen = col_b.selectbox("Senior Citizen", [0, 1])
            Partner = col_a.selectbox("Has Partner?", ["Yes", "No"])
            Dependents = col_b.selectbox("Has Dependents?", ["Yes", "No"])

        with tab2:
            col_c, col_d = st.columns(2)
            PhoneService = col_c.selectbox("Phone Service", ["Yes", "No"])
            MultipleLines = col_d.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
            InternetService = col_c.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
            OnlineSecurity = col_d.selectbox("Online Security", ["Yes", "No", "No internet service"])
            OnlineBackup = col_c.selectbox("Online Backup", ["Yes", "No", "No internet service"])
            DeviceProtection = col_d.selectbox("Device Protection", ["Yes", "No", "No internet service"])
            TechSupport = col_c.selectbox("Tech Support", ["Yes", "No", "No internet service"])
            StreamingTV = col_d.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
            StreamingMovies = col_c.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

        with tab3:
            col_e, col_f = st.columns(2)
            tenure = col_e.number_input("Tenure (months)", 0, 120, 5)
            monthly_charges = col_f.number_input("Monthly Charges ($)", 0.0, 500.0, 75.0)
            Contract = col_e.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
            PaperlessBilling = col_f.selectbox("Paperless Billing", ["Yes", "No"])
            PaymentMethod = col_e.selectbox("Payment Method",
                                         ["Electronic check", "Mailed check",
                                          "Bank transfer (automatic)", "Credit card (automatic)"])

        include_explanation = st.checkbox("🔍 Generate AI Insights (SHAP Explainer)", value=True)
        submitted = st.form_submit_button("🚀 Assess Churn Risk")

    if submitted:
        payload = {
            "customer": {
                "gender": gender,
                "SeniorCitizen": SeniorCitizen,
                "Partner": Partner,
                "Dependents": Dependents,
                "PhoneService": PhoneService,
                "MultipleLines": MultipleLines,
                "InternetService": InternetService,
                "OnlineSecurity": OnlineSecurity,
                "OnlineBackup": OnlineBackup,
                "DeviceProtection": DeviceProtection,
                "TechSupport": TechSupport,
                "StreamingTV": StreamingTV,
                "StreamingMovies": StreamingMovies,
                "tenure": tenure,
                "MonthlyCharges": monthly_charges,
                "Contract": Contract,
                "PaperlessBilling": PaperlessBilling,
                "PaymentMethod": PaymentMethod,
                "TotalCharges": monthly_charges * tenure # Approximation
            },
            "business_config": business_config,
            "include_explanation": include_explanation
        }

        with st.spinner("Analyzing customer behavior..."):
            response = predict_single(payload)

        if response.status_code == 200:
            result = response.json()
        
            st.success("Analysis Complete")
        
            # Results Metrics
            m1, m2, m3, m4 = st.columns(4)
            p_churn = result["prediction"]["p_churn"]
            m1.metric("Churn Risk", f"{p_churn*100:.1f}%")
            m2.metric("Risk Segment", result["prediction"]["segment"])
            m3.metric("Economic Gain", f"${result['business_metrics']['expected_gain']:.2f}")
            m4.metric("Action", result["business_metrics"]["decision"])
            
            st.divider()

            col_left, col_right = st.columns([1, 1.2])

            with col_left:
                st.subheader("💡 Business Recommendation")
                decision = result["business_metrics"]["decision"]
                segment = result["prediction"]["segment"]
                
                rec_html = f"""
                <div class="recommendation-box">
                    <div class="recommendation-title">Strategic Action: {decision}</div>
                    <p>This customer is classified as <b>{segment}</b>.</p>
                    <p>{"The potential life-time value recovery justifies an intervention." if decision == "Retain" else "The cost of intervention outweighs the expected recovery value."}</p>
                </div>
                """
                st.markdown(rec_html, unsafe_allow_html=True)
                
                st.write("**Key Stats:**")
                st.write(f"- **Current Tenure:** {tenure} months")
                st.write(f"- **Monthly Revenue:** ${monthly_charges:.2f}")
                st.write(f"- **Max Recovery Value (BRV):** ${result['business_metrics']['BRV']:.2f}")

            with col_right:
                if result["explanation"] is not None:
                    st.subheader("🔍 Top Risk Drivers")
                    exp_df = pd.DataFrame(result["explanation"]["top_features"])
                    # Use Plotly for interactive bar chart
                    fig = px.bar(
                        exp_df, 
                        x="impact", 
                        y="feature", 
                        orientation='h',
                        color='impact',
                        color_continuous_scale='RdYlGn_r',
                        labels={"impact": "Impact on Churn Risk", "feature": "Feature"},
                        template="simple_white"
                    )
                    fig.update_layout(showlegend=False, height=350, margin=dict(l=20, r=20, t=20, b=20))
                    st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.error(f"API Error: {response.json().get('detail', 'Unknown error')}")