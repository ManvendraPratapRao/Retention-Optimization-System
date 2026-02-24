import json
import pandas as pd
import logging
from typing import Dict, Tuple
from app.config import BusinessConfig

logger = logging.getLogger(__name__)


# ==============================
# Load Segmentation Config
# ==============================

def load_segmentation_config(
    path: str = "models/segmentation_config.json"
) -> Dict:
    with open(path, "r") as f:
        return json.load(f)


# ==============================
# Core Calculations
# ==============================

def calculate_base_remaining_value(
    tenure: float,
    monthly_charges: float,
    config: BusinessConfig
) -> Tuple[float, float]:

    if tenure < 0 or monthly_charges < 0:
        raise ValueError("Invalid economic inputs")

    if monthly_charges == 0:
        return 0.0, 0.0

    base_months = max(config.avg_lifetime - tenure, config.floor_months)
    monthly_margin = monthly_charges * config.margin_pct
    brv = base_months * monthly_margin

    return brv, monthly_margin


def calculate_expected_gain(
    p_churn: float,
    brv: float,
    config: BusinessConfig
) -> Tuple[float, float, float]:

    expected_recovered = brv * p_churn * config.retention_success_rate
    retention_cost = config.retention_cost

    expected_gain = expected_recovered - retention_cost
    roi = expected_gain / retention_cost if retention_cost > 0 else 0

    return expected_gain, roi, retention_cost


def make_decision(expected_gain: float) -> str:
    return "Retain" if expected_gain > 0 else "Let Go"


# ==============================
# Segmentation
# ==============================

def assign_segment(
    p_churn: float,
    brv: float,
    median_brv: float,
    churn_threshold: float
) -> str:

    if brv >= median_brv and p_churn >= churn_threshold:
        return "High Value - High Risk"
    elif brv >= median_brv and p_churn < churn_threshold:
        return "High Value - Low Risk"
    elif brv < median_brv and p_churn >= churn_threshold:
        return "Low Value - High Risk"
    else:
        return "Low Value - Low Risk"
    
# ==============================
# Batch Decision Engine
# ==============================

def run_decision_engine(df: pd.DataFrame, config: BusinessConfig) -> pd.DataFrame:

    seg_config = load_segmentation_config()
    median_brv = seg_config["median_brv"]
    churn_threshold = seg_config["churn_threshold"]

    results = []

    for idx, row in df.iterrows():
        try:
            if pd.isna(row["tenure"]) or pd.isna(row["MonthlyCharges"]):
                logger.warning(f"Skipping row {idx}: Missing data")
                continue

            brv, _ = calculate_base_remaining_value(
                float(row["tenure"]),
                float(row["MonthlyCharges"]),
                config
            )

            expected_gain, roi, retention_cost = calculate_expected_gain(
                float(row["p_churn"]),
                brv,
                config
            )

            decision = make_decision(expected_gain)

            segment = assign_segment(
                p_churn=row["p_churn"],
                brv=brv,
                median_brv=median_brv,
                churn_threshold=churn_threshold
            )

            results.append({
                "p_churn": row["p_churn"],
                "BRV": round(brv, 2),
                "Segment": segment,
                "Expected_Gain": round(expected_gain, 2),
                "ROI": round(roi, 2),
                "Decision": decision,
                "Retention_cost": retention_cost
            })

        except Exception as e:
            logger.warning(f"Skipping row {idx}: {str(e)}")
            continue

    return pd.DataFrame(results)

# ==============================
# Campaign Summary
# ==============================


def campaign_summary(df: pd.DataFrame) -> Dict:

    targeted = df[df["Decision"] == "Retain"]

    total_cost = targeted["Retention_cost"].sum()
    total_gain = targeted["Expected_Gain"].sum()
    roi = total_gain / (total_cost + 1e-6)

    segment_breakdown = (
        df.groupby("Segment")
        .size()
        .to_dict()
    )

    return {
        "Total_Customers": len(df),
        "Targeted_Customers": len(targeted),
        "Total_Cost": round(total_cost, 2),
        "Total_Expected_Gain": round(total_gain, 2),
        "Campaign_ROI": round(roi, 2),
        "Segment_Distribution": segment_breakdown
    }