# Modeling: Churn Prediction

This document provides technical details on the machine learning model, training approach, and performance metrics.

## Model Summary
The system currently utilizes an **XGBoost Classifier** (calibrated) as its primary inference engine. 

- **Target**: Whether a customer will churn within the next defined billing cycle (0 = Stay, 1 = Churn).
- **Features**: 20+ features covering demographics, services (Internet, Phone), and contract details.

## Probability Calibration
> [!IMPORTANT]
> Standard ML models often over- or under-estimate probabilities. For economic calculations (ROI), we need "True Probabilities."

We use **Isotonic Regression** or **Platt Scaling** to calibrate the model. This ensures that if the model predicts a `0.8` churn probability, exactly 80% of customers in that bucket actually churn.

## Performance Metrics
Based on the current validation set:
- **AUC-ROC**: ~0.84 (Strong ability to distinguish between churners and non-churners).
- **F1-Score**: ~0.62 (Balanced for cost-sensitive intervention).

| Metric | Score | Note |
| :--- | :--- | :--- |
| **Recall** | 0.81 | High recall ensures we catch most potential churners. |
| **Precision** | 0.52 | Lower precision is acceptable given our low-cost intervention strategy. |

## Feature Engineering
The model heavily relies on:
1. **Tenure**: Length of relationship (strongly negatively correlated with churn).
2. **Contract Type**: Month-to-month contracts are the highest risk driver.
3. **Total Charges**: Proxied through Monthly Charges and Tenure.
4. **Internet Service**: Fiber optic users show higher variance in churn behavior.
