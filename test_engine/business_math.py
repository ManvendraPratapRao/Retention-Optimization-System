def calculate_base_remaining_value(tenure, monthly_charges, config):
    """
    Calculates future profit we expect from the customer
    if they don't churn.
    """

    base_months = max(config.avg_lifetime - tenure, config.floor_months)
    monthly_margin = monthly_charges * config.margin_pct
    brv = base_months * monthly_margin

    return brv, monthly_margin