import streamlit as st
import pandas as pd

from components.api_client import predict_batch, predict_single


def render_batch_mode(business_config):

    st.subheader("Batch Customer Prediction")

    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is None:
        st.info("Please upload a CSV file.")
        return

    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head(), use_container_width=True)
    st.write(f"Total Rows Uploaded: {len(df)}")

    # -----------------------------------
    # RUN BATCH
    # -----------------------------------
    if st.button("Run Batch Prediction"):

        uploaded_file.seek(0)

        with st.spinner("Running batch prediction..."):
            response = predict_batch(uploaded_file, business_config)

        if response.status_code != 200:
            st.error(response.json().get("detail"))
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

        st.success("Batch Prediction Completed")

        st.subheader("Campaign Summary")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Customers", summary["Total_Customers"])
        col2.metric("Targeted Customers", summary["Targeted_Customers"])
        col3.metric("Campaign ROI", summary["Campaign_ROI"])

        col4, col5 = st.columns(2)
        col4.metric("Total Cost", summary["Total_Cost"])
        col5.metric("Total Expected Gain", summary["Total_Expected_Gain"])

        # ----------------------------------
        # 5️⃣ Segment Distribution Chart
        # ----------------------------------
        segment_data = summary.get("Segment_Distribution", {})

        if segment_data:
            st.subheader("Segment Distribution")

            segment_df = pd.DataFrame(
                list(segment_data.items()),
                columns=["Segment", "Count"]
            )

            st.bar_chart(segment_df.set_index("Segment"))
            
        # -----------------------------
        # FULL RESULTS
        # -----------------------------
        results_df = pd.DataFrame(result["results"])

        st.subheader("Full Results")
        st.dataframe(results_df, use_container_width=True)

        # -----------------------------
        # SHAP SECTION
        # -----------------------------
        st.subheader("Explain Specific Customer")

        selected_index = st.selectbox(
            "Select Row Index",
            options=results_df.index.tolist()
        )

        if st.button("Get SHAP Explanation"):

            selected_row = df_original.iloc[selected_index].to_dict()

            payload = {
                "customer": selected_row,
                "business_config": business_config,
                "include_explanation": True
            }

            with st.spinner("Generating SHAP..."):
                shap_response = predict_single(payload)

            if shap_response.status_code == 200:
                shap_result = shap_response.json()

                explanation = shap_result.get("explanation")

                if explanation:
                    st.subheader("Top Risk Drivers")
                    for feature in explanation["top_features"]:
                        st.write(
                            f"**{feature['feature']}** → {feature['impact']}"
                        )
                else:
                    st.warning("No explanation returned.")
            else:
                st.error(shap_response.json().get("detail"))