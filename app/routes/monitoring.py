from fastapi import APIRouter
import sqlite3
import pandas as pd
import numpy as np
import os
from app.core.monitoring import DB_PATH
from app.core.logger import logger

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@router.get("/summary")
async def get_summary():
    """Get aggregated monitoring statistics."""
    try:
        if not os.path.exists(DB_PATH):
            return {"status": "no_data", "message": "No monitoring data available yet."}

        conn = sqlite3.connect(DB_PATH)
        query = "SELECT * FROM predictions"
        df = pd.read_sql_query(query, conn)
        conn.close()

        if df.empty:
            return {"status": "no_data", "message": "Monitoring table is empty."}

        # Basic Aggregates
        summary = {
            "total_predictions": len(df),
            "avg_churn_prob": float(df["p_churn"].mean()),
            "risk_distribution": df["risk_segment"].value_counts().to_dict(),
            "decision_distribution": df["decision"].value_counts().to_dict(),
            "total_expected_gain": float(df["expected_gain"].sum()),
            "recent_volume": df.tail(100).groupby(df["timestamp"].str[:10]).size().to_dict() # Group by date
        }
        
        return summary
    except Exception as e:
        logger.error(f"Error fetching monitoring summary: {e}")
        return {"error": str(e)}

@router.get("/drift")
async def get_drift_stats():
    """Get basic feature distribution stats for drift detection."""
    try:
        if not os.path.exists(DB_PATH):
            return {"error": "No data"}

        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT features FROM predictions", conn)
        conn.close()

        import json
        # Parse features from JSON string
        features_list = [json.loads(x) for x in df["features"]]
        live_df = pd.DataFrame(features_list)

        # Focus on a key numerical feature for baseline comparison
        # In a real app, we'd compare against training data stats. 
        # Here we'll return the live distribution for 'MonthlyCharges'
        if "MonthlyCharges" in live_df.columns:
            counts, bins = np.histogram(live_df["MonthlyCharges"], bins=10)
            return {
                "feature": "MonthlyCharges",
                "counts": counts.tolist(),
                "bins": bins.tolist(),
                "mean": float(live_df["MonthlyCharges"].mean()),
                "std": float(live_df["MonthlyCharges"].std())
            }
        
        return {"message": "MonthlyCharges not found in feature logs."}

    except Exception as e:
        logger.error(f"Error fetching drift stats: {e}")
        return {"error": str(e)}
