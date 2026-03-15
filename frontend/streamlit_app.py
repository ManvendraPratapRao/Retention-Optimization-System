import streamlit as st
from pathlib import Path
from components.single_mode import render_single_mode
from components.sliders import business_sliders
from components.batch_mode import render_batch_mode

st.set_page_config(
    page_title="Churn Intelligence Dashboard",
    page_icon="🧠",
    layout="wide"
)

# Load CSS
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🛠 Settings")
business_config = business_sliders()

# Main Header
st.title("🧠 Churn Intelligence & Retention Dashboard")
st.markdown("""
Welcome to the **Retention Optimization Engine**. This system goes beyond simple predictions by 
combining **ML churn probabilities** with **economic decision logic** to suggest the most 
profitable retention actions.
""")

st.divider()

mode = st.tabs(["👤 Single Customer Prediction", "📂 Batch Analysis"])

with mode[0]:
    render_single_mode(business_config)

with mode[1]:
    render_batch_mode(business_config)