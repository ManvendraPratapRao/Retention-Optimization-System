import streamlit as st


def business_sliders():

    st.sidebar.header("Business Assumptions")

    avg_lifetime = st.sidebar.number_input("Avg Lifetime (months)", 1, 120, 36)
    floor_months = st.sidebar.number_input("Minimum Future Months", 0, 36, 6)

    margin_pct = st.sidebar.slider("Margin %", 0.0, 1.0, 0.5)
    retention_success_rate = st.sidebar.slider("Retention Success Rate", 0.0, 1.0, 0.2)

    contact_cost = st.sidebar.number_input("Contact Cost", 0.0, 100.0, 5.0)
    incentive_cost = st.sidebar.number_input("Incentive Cost", 0.0, 500.0, 20.0)

    return {
        "avg_lifetime": avg_lifetime,
        "floor_months": floor_months,
        "margin_pct": margin_pct,
        "retention_success_rate": retention_success_rate,
        "contact_cost": contact_cost,
        "incentive_cost": incentive_cost
    }