import streamlit as st
from components.single_mode import render_single_mode
from components.sliders import business_sliders
from components.batch_mode import render_batch_mode
st.set_page_config(page_title="Churn Retention System", layout="wide")

st.title("Churn Retention Optimization System")

mode = st.radio("Select Mode", ["Single Prediction", "Batch Prediction"])

business_config = business_sliders()

if mode == "Single Prediction":
    render_single_mode(business_config)

elif mode == "Batch Prediction":
    render_batch_mode(business_config)