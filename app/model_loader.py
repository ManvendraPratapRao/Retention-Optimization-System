import joblib
import pandas as pd
from pathlib import Path
import json
import os

from app.explainability import ShapExplainer
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class ModelLoader:
    """
    Loads and manages:
    - Trained ML pipeline
    - SHAP explainer
    - Model metadata
    """

    def __init__(self):
        # ------------------------------------------------
        # 1️⃣ Path Resolution
        # ------------------------------------------------
        model_env_path = os.getenv("MODEL_PATH", "models/churn_pipeline.pkl")
        metadata_env_path = os.getenv("METADATA_PATH", "models/metadata.json")
        background_env_path = os.getenv("BACKGROUND_PATH", "models/background_sample.csv")

        # Support both absolute and relative paths from BASE_DIR
        model_path = Path(model_env_path) if os.path.isabs(model_env_path) else BASE_DIR / model_env_path
        metadata_path = Path(metadata_env_path) if os.path.isabs(metadata_env_path) else BASE_DIR / metadata_env_path
        background_path = Path(background_env_path) if os.path.isabs(background_env_path) else BASE_DIR / background_env_path

        # -----------------------------
        # 2️⃣ Pipeline Loading & Validation
        # -----------------------------
        if not model_path.exists():
            raise FileNotFoundError(
                f"🚨 Critical: Model file not found at {model_path}. "
                "Check MODEL_PATH environment variable."
            )

        try:
            self.pipeline = joblib.load(model_path)
            # Basic validation
            if not hasattr(self.pipeline, "predict_proba"):
                raise TypeError(f"Loaded artifact at {model_path} is not a valid predictor (missing predict_proba).")
        except Exception as e:
            raise RuntimeError(f"Failed to load model pipeline from {model_path}: {str(e)}")

        # -----------------------------
        # 3️⃣ Metadata Integration
        # -----------------------------
        if metadata_path.exists():
            try:
                with open(metadata_path, "r") as f:
                    self.metadata = json.load(f)
            except json.JSONDecodeError:
                self.metadata = {"model_version": "corrupt", "message": "metadata.json is not valid JSON"}
        else:
            self.metadata = {"model_version": "unknown", "message": "No metadata.json file found"}

        # -----------------------------
        # 4️⃣ SHAP Initialization
        # -----------------------------
        if background_path.exists():
            try:
                background_df = pd.read_csv(background_path)
                self.explainer = ShapExplainer(self.pipeline, background_df)
            except Exception as e:
                # We don't want to crash the whole app if only SHAP fails
                self.explainer = None
        else:
            self.explainer = None

    # ------------------------------------------------
    # Public Methods
    # ------------------------------------------------

    def predict_proba(self, df: pd.DataFrame):
        """
        Returns probability of churn (positive class).
        """
        return self.pipeline.predict_proba(df)[:, 1]

    def explain(self, df: pd.DataFrame):
        """
        Returns SHAP explanation for single row.
        """
        if self.explainer is None:
            raise RuntimeError("SHAP explainer not initialized.")
        return self.explainer.explain(df)


# ------------------------------------------------
# Singleton Instance
# ------------------------------------------------
model_loader = ModelLoader()