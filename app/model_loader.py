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
        # 1️⃣ Load Model Path from ENV (with fallback)
        # ------------------------------------------------
        model_env_path = os.getenv("MODEL_PATH", "models/churn_pipeline.pkl")
        metadata_env_path = os.getenv("METADATA_PATH", "models/metadata.json")
        background_env_path = os.getenv("BACKGROUND_PATH", "models/background_sample.csv")

        model_path = BASE_DIR / model_env_path
        metadata_path = BASE_DIR / metadata_env_path
        background_path = BASE_DIR / background_env_path

        # -----------------------------
        # 2️⃣ Load Pipeline
        # -----------------------------
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")

        self.pipeline = joblib.load(model_path)

        # -----------------------------
        # 3️⃣ Load Metadata
        # -----------------------------
        if metadata_path.exists():
            with open(metadata_path, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                "model_version": "unknown",
                "message": "No metadata.json found"
            }

        # -----------------------------
        # 4️⃣ Load SHAP Background
        # -----------------------------
        if background_path.exists():
            background_df = pd.read_csv(background_path)
            self.explainer = ShapExplainer(self.pipeline, background_df)
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