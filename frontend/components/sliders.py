import streamlit as st


def business_sliders():

    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 Economic Assumptions")

    avg_lifetime = st.sidebar.number_input(
        "Avg Lifetime (months)", 1, 120, 36,
        help="The expected total duration a typical customer stays with the company."
    )
    floor_months = st.sidebar.number_input(
        "Min Future Months", 0, 36, 6,
        help="The minimum months of value we expect to recover if a retention effort succeeds."
    )

    margin_pct = st.sidebar.slider(
        "Margin %", 0.0, 1.0, 0.5,
        help="The percentage of monthly charges that is profit (after operational costs)."
    )
    retention_success_rate = st.sidebar.slider(
        "Retention Success Rate", 0.0, 1.0, 0.2,
        help="The probability that a customer will stay if we intervene."
    )

    st.sidebar.subheader("📈 Intervention Costs")
    contact_cost = st.sidebar.number_input(
        "Contact Cost", 0.0, 100.0, 5.0,
        help="Cost of call/SMS/email outreach."
    )
    incentive_cost = st.sidebar.number_input(
        "Incentive Cost", 0.0, 500.0, 20.0,
        help="Cost of the discount or gift offered to the customer."
    )

    return {
        "avg_lifetime": avg_lifetime,
        "floor_months": floor_months,
        "margin_pct": margin_pct,
        "retention_success_rate": retention_success_rate,
        "contact_cost": contact_cost,
        "incentive_cost": incentive_cost
    }