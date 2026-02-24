from business_math import calculate_base_remaining_value

def _safe_float(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except:
        return default


def compute_customer_value(user_data, config):

    tenure = _safe_float(user_data.get("tenure"))
    monthly_charges = _safe_float(user_data.get("MonthlyCharges"))

    brv, monthly_margin = calculate_base_remaining_value(
        tenure,
        monthly_charges,
        config
    )

    return {
        "brv": round(brv, 2),
        "monthly_margin": round(monthly_margin, 2)
    }