import streamlit as st
import pandas as pd
import plotly.express as px
from components.api_client import predict_batch, predict_single


def render_batch_mode(business_config):

    st.subheader("📂 Fleet-Wide Churn Analysis")
    st.markdown("Upload a customer dataset to run batch predictions and estimate total campaign ROI.")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"], help="Ensure the CSV follows the Telco Churn schema.")

    if uploaded_file is None:
        st.info("💡 Pro Tip: Upload a CSV containing multiple customer records to see the aggregate economic impact.")
        return

    df = pd.read_csv(uploaded_file)

    with st.expander("🔍 Preview Uploaded Data"):
        st.dataframe(df.head(), use_container_width=True)
        st.write(f"Total Records: **{len(df)}**")

    # -----------------------------------
    # RUN BATCH
    # -----------------------------------
    if st.button("🚀 Run Comprehensive Batch Prediction"):

        uploaded_file.seek(0)

        with st.spinner("Processing large-scale churn analysis..."):
            response = predict_batch(uploaded_file, business_config)

        if response.status_code != 200:
            st.error(f"Batch Processing Error: {response.json().get('detail', 'Unknown error')}")
            return

        result = response.json()

        # 🔥 STORE IN SESSION STATE
        st.session_state["batch_results"] = result
        st.session_state["original_df"] = df

    # -----------------------------------
    # DISPLAY RESULTS IF AVAILABLE
    # -----------------------------------
    if "batch_results" in st.session_state:

        result = st.session_state["batch_results"]
        df_original = st.session_state["original_df"]
        summary = result["summary"]

        st.success("Analysis Complete: Strategy Optimized")

        st.divider()

        # -----------------------------
        # 1️⃣ Campaign Summary
        # -----------------------------
        st.subheader("📊 Strategic Campaign Summary")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Campaign ROI", f"{summary['Campaign_ROI']:.1f}x")
        m2.metric("Targeted Customers", summary["Targeted_Customers"])
        m3.metric("Success Multiplier", f"{business_config['retention_success_rate']*100:.0f}%", help="Based on your retention success assumption")

        m4, m5 = st.columns(2)
        m4.metric("Total Intervention Cost", f"${summary['Total_Cost']:,.2f}")
        m5.metric("Net Expected Gain", f"${summary['Total_Expected_Gain']:,.2f}", delta=f"{summary['Total_Expected_Gain'] - summary['Total_Cost']:,.0f} Profit")

        st.divider()

        # -----------------------------
        # 2️⃣ Charts & Tables
        # -----------------------------
        col_chart, col_table = st.columns([1, 1.2])

        with col_chart:
            segment_data = summary.get("Segment_Distribution", {})
            if segment_data:
                st.subheader("📈 Segment Distribution")
                segment_df = pd.DataFrame(
                    list(segment_data.items()),
                    columns=["Segment", "Count"]
                )
                fig_seg = px.pie(
                    segment_df, 
                    values='Count', 
                    names='Segment',
                    color_discrete_sequence=px.colors.qualitative.Safe,
                    hole=0.4
                )
                fig_seg.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=350)
                st.plotly_chart(fig_seg, use_container_width=True)

        with col_table:
            st.subheader("📋 Top Risk Targets")
            results_df = pd.DataFrame(result["results"])
            st.dataframe(
                results_df.sort_values("p_churn", ascending=False).head(10), 
                use_container_width=True
            )
            
            # Export
            csv = results_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Full Results as CSV",
                data=csv,
                file_name="churn_batch_predictions.csv",
                mime="text/csv",
            )

        st.divider()

        # -----------------------------
        # 3️⃣ SHAP Investigation
        # -----------------------------
        st.subheader("🔎 Deep Dive: Individual Risk Analysis")
        st.markdown("Select a specific customer from the batch to understand their individual risk drivers.")

        selected_index = st.selectbox(
            "Select Customer Index (Row #)",
            options=results_df.index.tolist()
        )

        if st.button("Generate SHAP Explanation"):
            selected_row = df_original.iloc[selected_index].to_dict()
            payload = {
                "customer": selected_row,
                "business_config": business_config,
                "include_explanation": True
            }

            with st.spinner("Decoding black-box model..."):
                shap_response = predict_single(payload)

            if shap_response.status_code == 200:
                shap_result = shap_response.json()
                explanation = shap_result.get("explanation")

                if explanation:
                    st.subheader(f"Risk Profile for Customer #{selected_index}")
                    exp_df = pd.DataFrame(explanation["top_features"])
                    fig_ind = px.bar(
                        exp_df, 
                        x="impact", 
                        y="feature", 
                        orientation='h',
                        color='impact',
                        color_continuous_scale='RdYlGn_r',
                        template="simple_white"
                    )
                    fig_ind.update_layout(showlegend=False, height=300)
                    st.plotly_chart(fig_ind, use_container_width=True)
                else:
                    st.warning("Decision engine logic did not trigger an explanation for this instance.")
            else:
                st.error("SHAP service encountered an issue.")