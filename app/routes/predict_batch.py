from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import pandas as pd
import io

from app.model_loader import model_loader
from app.config import BusinessConfig
from app.decision_engine import run_decision_engine, campaign_summary
from app.core.logger import logger

router = APIRouter()

REQUIRED_COLUMNS = [
    "tenure",
    "MonthlyCharges",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "Contract",
    "PaymentMethod",
    "PaperlessBilling",
    "InternetService",
    "TechSupport",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "StreamingTV",
    "StreamingMovies"
]


@router.post("/predict-batch")
async def predict_batch(
    file: UploadFile = File(...),
    avg_lifetime: int = Form(36),
    floor_months: int = Form(6),
    margin_pct: float = Form(0.5),
    retention_success_rate: float = Form(0.2),
    contact_cost: float = Form(5.0),
    incentive_cost: float = Form(20.0),
):
    try:
        logger.info("Batch prediction request received")

        # -----------------------------
        # 1️⃣ Read CSV
        # -----------------------------
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        if df.empty:
            raise ValueError("Uploaded CSV is empty.")

        logger.info(f"Rows received: {len(df)}")

        # -----------------------------
        # 2️⃣ Validate required columns
        # -----------------------------
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # -----------------------------
        # 3️⃣ Convert numeric columns
        # -----------------------------
        df["tenure"] = pd.to_numeric(df["tenure"], errors="coerce")
        df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors="coerce")

        # -----------------------------
        # 4️⃣ Predict churn probability
        # -----------------------------
        p_churn = model_loader.predict_proba(df)
        df["p_churn"] = p_churn

        # -----------------------------
        # 5️⃣ Build business config
        # -----------------------------
        business_config = BusinessConfig(
            avg_lifetime=avg_lifetime,
            floor_months=floor_months,
            margin_pct=margin_pct,
            retention_success_rate=retention_success_rate,
            contact_cost=contact_cost,
            incentive_cost=incentive_cost,
        )

        business_config.validate_config()

        # -----------------------------
        # 6️⃣ Run decision engine
        # -----------------------------
        decision_df = run_decision_engine(df, business_config)

        if decision_df.empty:
            raise ValueError("No valid rows after processing.")

        # -----------------------------
        # 7️⃣ Campaign summary
        # -----------------------------
        summary = campaign_summary(decision_df)

        logger.info("Batch processing completed successfully")

        # -----------------------------
        # 8️⃣ Return response
        # -----------------------------
        return {
            "api_version": "1.0.0",
            "model_version": model_loader.metadata.get("model_version"),
            "summary": summary,
            "results": decision_df.to_dict(orient="records"),
            "total_processed_rows": len(decision_df)
        }

    except ValueError as ve:
        logger.error(f"Validation error in batch: {str(ve)}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "ValidationError",
                "message": str(ve)
            }
        )

    except Exception as e:
        logger.error(f"Unexpected batch error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred."
            }
        )