# Explainability: SHAP Risk Drivers

This document explains how the system interprets its "black box" machine learning predictions for human stakeholders.

## What is SHAP?
The system uses **SHAP (SHapley Additive exPlanations)** to break down a specific churn probability into contribution scores for each feature.

- **Positive SHAP Value**: This feature is **increasing** the risk of churn.
- **Negative SHAP Value**: This feature is **decreasing** the risk (driving loyalty).

## Interpreting the Dashboard
In the "Single Customer Prediction" tab, you will see a waterfall chart (powered by Plotly) labeled **"Key Risk Drivers."**

### Common Scenarios

| Feature | Direction | Interpretation |
| :--- | :--- | :--- |
| **Contract_Month-to-month** | ⬆️ Increasing | High risk. Suggest moving the customer to a 1-year contract. |
| **InternetService_Fiber** | ⬆️ Increasing | Potential service quality issue or pricing pressure in that segment. |
| **Tenure_Low** | ⬆️ Increasing | New customers are in the "onboarding danger zone." |
| **Partner_Yes** | ⬇️ Decreasing | Multi-user households are more "sticky" and loyal. |

## Global vs. Local Explanations
1. **Local (Single Mode)**: Focuses on the *why* for one specific person.
2. **Global (Batch Mode)**: Summarizes the *why* for an entire segment or campaign (visible in the "Batch Analysis" overview).

## Business Action
Agents should use these drivers to tailor their conversation. If the driver is "MonthlyCharges," focus on discounts. If the driver is "InternetService," focus on technical support or speed upgrades.
