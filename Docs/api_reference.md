# API Reference: Churn Intelligence Platform

This document describes the primary API endpoints available in the backend service.

## Base URL
The backend runs by default at `http://localhost:8000`.

---

## 1. Prediction Endpoints

### 🔹 POST `/predict-single`
Performs a churn analysis for a single customer record.

**Request Body:**
```json
{
  "customer": {
    "tenure": 12,
    "MonthlyCharges": 75.0,
    "Contract": "Month-to-month",
    "InternetService": "Fiber optic",
    ...
  },
  "business_config": {
    "avg_lifetime": 36,
    "margin_pct": 0.5,
    "retention_success_rate": 0.2,
    "contact_cost": 5.0,
    "incentive_cost": 20.0
  },
  "include_explanation": true
}
```

**Response:**
Returns a JSON object containing `prediction` (probability/segment), `business_metrics` (ROI/Action), and `explanation` (SHAP).

---

### 🔹 POST `/predict-batch`
Accepts a CSV file of customer data and returns a full campaign analysis.

---

## 2. Health & Monitoring Endpoints

### 🔹 GET `/health`
Returns system status and model metadata.

**Response:**
```json
{
  "status": "healthy",
  "model_version": "1.0.0",
  "timestamp": "..."
}
```

---

### 🔹 GET `/monitoring/summary`
Returns aggregate statistics from the persistent monitoring database.

---

### 🔹 GET `/monitoring/drift`
Returns current distribution statistics for key features (e.g., MonthlyCharges) to help track data drift over time.
