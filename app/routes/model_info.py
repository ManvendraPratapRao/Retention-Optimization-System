from fastapi import APIRouter
from app.model_loader import model_loader

router = APIRouter()


@router.get("/model-info")
def get_model_info():

    metadata = model_loader.metadata

    return {
        "api_version": "1.0.0",
        "status": "ok",
        "model_name": metadata.get("model_name"),
        "model_version": metadata.get("model_version"),
        "training_date": metadata.get("training_date"),
        "roc_auc": metadata.get("roc_auc"),
        "best_threshold": metadata.get("best_threshold"),
        "features_used": metadata.get("features_used"),
        "shap_enabled": model_loader.explainer is not None
    }