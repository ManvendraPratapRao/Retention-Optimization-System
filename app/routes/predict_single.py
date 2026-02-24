from fastapi import APIRouter, HTTPException
import pandas as pd

from app.schemas import SingleRequest
from app.model_loader import model_loader
from app.config import BusinessConfig
from app.decision_engine import (
    calculate_base_remaining_value,
    calculate_expected_gain,
    make_decision,
    load_segmentation_config,
    assign_segment
)

from app.core.logger import logger


router = APIRouter()


@router.post("/predict-single")
def predict_single(request: SingleRequest):
    try:
        logger.info("Single prediction request received")

        # -----------------------------
        # 1️⃣ Extract customer data
        # -----------------------------
        customer_dict = request.customer.model_dump()
        df = pd.DataFrame([customer_dict])

        # -----------------------------
        # 2️⃣ Predict churn probability
        # -----------------------------
        p_churn = float(model_loader.predict_proba(df)[0])
        logger.info(f"Predicted churn probability: {round(p_churn, 4)}")

        # -----------------------------
        # 3️⃣ Convert business config
        # -----------------------------
        business_config = BusinessConfig(
            **request.business_config.model_dump()
        )
        business_config.validate_config()

        # -----------------------------
        # 4️⃣ Calculate BRV
        # -----------------------------
        brv, monthly_margin = calculate_base_remaining_value(
            tenure=df["tenure"].iloc[0],
            monthly_charges=df["MonthlyCharges"].iloc[0],
            config=business_config
        )

        # -----------------------------
        # 5️⃣ Calculate expected gain
        # -----------------------------
        expected_gain, roi, retention_cost = calculate_expected_gain(
            p_churn=p_churn,
            brv=brv,
            config=business_config
        )

        decision = make_decision(expected_gain)

        # -----------------------------
        # 6️⃣ Segmentation
        # -----------------------------
        seg_config = load_segmentation_config()
        segment = assign_segment(
            p_churn=p_churn,
            brv=brv,
            median_brv=seg_config["median_brv"],
            churn_threshold=seg_config["churn_threshold"]
        )

        # -----------------------------
        # 7️⃣ Optional SHAP Explanation
        # -----------------------------
        explanation = None

        if request.include_explanation:
            logger.info("Generating SHAP explanation")
            explanation = model_loader.explain(df)

        # -----------------------------
        # 8️⃣ Return response
        # -----------------------------
        return {
            "api_version": "1.0.0",
            "model_version": model_loader.metadata.get("model_version"),
            "prediction": {
                "p_churn": round(p_churn, 4),
                "segment": segment
            },
            "business_metrics": {
                "BRV": round(brv, 2),
                "monthly_margin": round(monthly_margin, 2),
                "expected_gain": round(expected_gain, 2),
                "ROI": round(roi, 2),
                "retention_cost": retention_cost,
                "decision": decision
            },
            "explanation": explanation
        }

    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "ValidationError",
                "message": str(ve)
            }
        )

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred."
            }
        )