import shap
import numpy as np


class ShapExplainer:

    def __init__(self, pipeline, background_data):

        self.pipeline = pipeline

        # Explicit step names (safer)
        self.preprocessor = pipeline.named_steps["preprocessor"]
        self.model = pipeline.named_steps["model"]

        # Sample background for speed
        background_sample = background_data.sample(
            min(100, len(background_data)),
            random_state=42
        )

        background_processed = self.preprocessor.transform(background_sample)

        self.explainer = shap.Explainer(
            self._predict_proba_processed,
            background_processed
        )

    def _predict_proba_processed(self, processed_data):
        return self.model.predict_proba(processed_data)[:, 1]

    def explain(self, input_df):

        processed_input = self.preprocessor.transform(input_df)

        shap_values = self.explainer(processed_input)

        values = shap_values.values[0]
        base_value = float(np.round(shap_values.base_values[0], 5))

        feature_names = self.preprocessor.get_feature_names_out()

        top_features = sorted(
            zip(feature_names, values),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:3]

        return {
            "base_value": base_value,
            "top_features": [
                {
                    "feature": str(feature),
                    "impact": float(np.round(value, 5))
                }
                for feature, value in top_features
            ]
        }