import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def render_monitoring_mode():
    st.subheader("📈 ML System Health & Monitoring")
    st.markdown("Real-time observability into model performance, risk concentration, and data drift.")

    # 1. Fetch Summary
    try:
        response = requests.get(f"{BASE_URL}/monitoring/summary")
        if response.status_code != 200:
            st.error("Could not fetch monitoring data.")
            return
        
        data = response.json()
        if data.get("status") == "no_data":
            st.warning(data["message"])
            return

        # Top level Metrics
        st.divider()
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Predictions", data["total_predictions"])
        m2.metric("Avg Churn Prob", f"{data['avg_churn_prob']*100:.1f}%")
        m3.metric("Total ROI Gain", f"${data['total_expected_gain']:,.0f}")
        m4.metric("Active Model", "Churn-v1 (Calibrated)")

        st.divider()

        # 2. Key Visualizations
        col_risk, col_vol = st.columns(2)

        with col_risk:
            st.subheader("Risk Segment Concentration")
            risk_dist = data["risk_distribution"]
            risk_df = pd.DataFrame(list(risk_dist.items()), columns=["Segment", "Count"])
            fig_risk = px.pie(
                risk_df, values='Count', names='Segment',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.4
            )
            st.plotly_chart(fig_risk, use_container_width=True)

        with col_vol:
            st.subheader("Prediction Volume (Last 30 Days)")
            vol_data = data["recent_volume"]
            vol_df = pd.DataFrame(list(vol_data.items()), columns=["Date", "Volume"]).sort_values("Date")
            fig_vol = px.line(vol_df, x="Date", y="Volume", markers=True, template="simple_white")
            st.plotly_chart(fig_vol, use_container_width=True)

        st.divider()

        # 3. Drift Analysis
        st.subheader("📡 Feature Drift Watch")
        drift_resp = requests.get(f"{BASE_URL}/monitoring/drift")
        if drift_resp.status_code == 200:
            drift_data = drift_resp.json()
            if "counts" in drift_data:
                col_info, col_chart = st.columns([1, 2])
                with col_info:
                    st.write(f"**Target Feature:** `{drift_data['feature']}`")
                    st.write(f"**Live Mean:** {drift_data['mean']:.2f}")
                    st.write(f"**Live Std:** {drift_data['std']:.2f}")
                    st.info("System is monitoring distribution shifts against training baseline.")
                
                with col_chart:
                    # Construct histogram from bins/counts
                    hist_df = pd.DataFrame({
                        "Bin": drift_data["bins"][:-1],
                        "Volume": drift_data["counts"]
                    })
                    fig_drift = px.bar(hist_df, x="Bin", y="Volume", title="Live Input Distribution", template="simple_white")
                    st.plotly_chart(fig_drift, use_container_width=True)
            else:
                st.info("Additional drift data will populate as more predictions are logged.")

    except Exception as e:
        st.error(f"Monitoring service unavailable: {e}")
