Link to the webapp: [https://github.com/ManvendraPratapRao/Retention-Optimization-System](https://retention-optimization-system.streamlit.app/)

## 🚀 Retention Optimization System ##

  
A production-ready Churn Prediction & Retention Optimization Engine built with:

- 🧠 Machine Learning (Calibrated Classification Model)
- 💰 Economic Decision Engine
-  🔍 SHAP Explainability
- ⚡ FastAPI Backend
- 📊 Streamlit Frontend
- 🐳 Dockerized Deployment
- ☁️ Render Cloud Deployment
  
This system predicts customer churn probability and translates it into economically optimized retention actions.
  
---

## 📌 Overview ##

Customer churn is one of the most classical problems in subscription-based businesses. However, predicting churn alone is not enough.

This system goes beyond classification by:

- Predicting churn probability
- Calibrating output probabilities
- Segmenting risk levels
- Applying economic logic
- Suggesting retention actions
- Providing SHAP-based explanations

It is designed as a modular production ML system, not just a notebook experiment.

---

## 💼 Business Value

Most churn projects stop at prediction.
This system goes further — it transforms predictions into **actionable retention strategies**.

### 📉 1. Revenue Protection

By identifying high-risk customers early, the system enables proactive intervention, reducing revenue leakage.

---

### 🎯 2. Smart Retention Spend

Not every at-risk customer should receive the same incentive.

The decision engine:

- Segments customers by churn probability
- Applies business thresholds
- Aligns intervention strength with expected economic return

This prevents:
- Overspending on low-risk customers
- Under-investing in high-value churn cases

---

### 📊 3. Data-Driven Retention Strategy

Instead of intuition-based offers, this system provides:
- Risk segment classification
- Probability-based prioritization
- Transparent reasoning via SHAP
Retention becomes measurable and optimizable.

---

### 🔍 4. Explainable Decision Making

Executives and retention teams can see:
- Why a customer is predicted to churn
- Which features drive that prediction    
This builds trust in AI-assisted decision systems.


---
## 🌟 What Makes This Project Unique

This is NOT just a churn prediction API.
It differentiates itself in 5 major ways:

### 1️⃣ Economic Decision Layer on Top of ML
Most ML projects return:
Churn Probability = 0.78
This system returns:
- Probability
- Risk segment
- Business action
- Economic reasoning

This bridges the gap between:  
**Data Science → Business Strategy**

Detailed explanation: `docs/decision_engine.md`

---

### 2️⃣ Probability Calibration

Instead of raw classifier outputs, the model uses calibrated probabilities, making:
- Threshold decisions more reliable
- Economic segmentation meaningful
- Risk-based strategies stable
Calibration is often ignored in portfolio projects — here it’s core.

---

### 3️⃣ Built for Production, Not Just a Notebook

This project includes:
- Modular FastAPI backend
- Separated business logic layer
- Pydantic validation
- Dockerized containers
- Streamlit UI
- Unit tests
- Cloud-ready deployment
It demonstrates system design capability — not just modeling.

---

### 4️⃣ Explainability as a First-Class Component

SHAP is not added as an afterthought.
It is integrated directly into the prediction flow:
Prediction → Business Logic → SHAP Explanation → API Response
This makes the system enterprise-ready.
 
 Details: `docs/explainability.md`
 
---
### 5️⃣ End-to-End ML Lifecycle

This repository includes:
- Problem framing
- EDA
- Feature engineering
- Model training
- Calibration
- Economic modeling
- API engineering
- Frontend integration
- Deployment
It demonstrates full applied ML maturity.

---
## 🧠 Strategic Impact

In a real telecom or SaaS environment, this system enables:
- Targeted retention campaigns
- ROI-aware discount allocation
- Customer risk prioritization
- Transparent AI governance
- Scalable API-based integration

It can serve as the backbone of a retention intelligence platform.

---

## 🏗 System Architecture
```
Client (Streamlit UI / External API)
            ↓
        FastAPI Backend
            ↓
      Pydantic Validation
            ↓
        Preprocessor
            ↓
    Calibrated ML Model
            ↓
      Decision Engine
            ↓
     SHAP Explainability
            ↓
        JSON Response
```

---
## 🧠 Model Overview

- Dataset: Telco Customer Churn
- Pipeline: Preprocessing + Calibrated Classifier
- Calibration: Probability calibration for decision reliability
- Output: Churn probability (0–1)
Evaluation metrics (see `docs/modeling.md`):
- ROC-AUC
- Confusion Matrix
- Precision / Recall
- Threshold tuning analysis
---
## 📡 API Endpoints

### 🔹 POST /predict
Single customer prediction.
### Request
```JSON
{  
  "tenure": 5,  
  "monthly_charges": 70.5,  
  ...  
}
```
### Response
```json
{  
  "churn_probability": 0.78,  
  "risk_segment": "High",  
  "recommended_action": "Aggressive retention offer",  
  "shap_explanation": {...}  
}
```

---
### 🔹 POST /predict-batch

Upload CSV for batch prediction.
Returns:
- Predictions
- Risk segments
- Business actions

Full contract available in: `docs/api_contract.md`

---

## 🖥 Frontend (Streamlit)

Location:
frontend/
Features:
- Single prediction form
- Batch upload mode
- Economic slider adjustments
- Clean modular UI components
- API abstraction via `api_client.py`

---
## 🐳 Run with Docker (Recommended)

### 1️⃣ Build & Start

```Docker
docker-compose up --build
```
Backend:
```
http://localhost:8000
```
Frontend:
```
http://localhost:8501
```
---
## 🛠 Local Development

### Backend

pip install -r requirements.txt  
uvicorn app.main:app --reload

### Frontend

streamlit run frontend/streamlit_app.py

---
## ☁️ Deployment (Render)

The system is designed for container-based deployment.
Backend:
- Build command: Dockerfile
- Start command: Uvicorn

Frontend:
- Separate container via `Dockerfile.frontend`
Environment variables are configured via `.env`.
See: docs/deployment.md

---
## 📊 Documentation
Detailed technical documentation available in:
- `docs/architecture.md`
- `docs/modeling.md`
- `docs/api_contract.md`
- `docs/decision_engine.md`
- `docs/explainability.md`
- `docs/deployment.md`

---
## 🔮 Future Improvements

- Model monitoring & drift detection
- Database integration
- Authentication layer
- A/B testing retention strategies
- Real-time streaming inference
- Business ROI dashboard

---

## 🎯 Production Highlights

- Modular backend architecture
- Clear separation of concerns
- Business logic layer on top of ML
- Explainable predictions
- Fully containerized
- Deployment-ready
- logging

---
## 🏆 Positioning

This project demonstrates capabilities in:

- Applied Machine Learning
- Backend System Design
- Business Logic Integration
- Explainable AI
- Containerized Deployment
- Production Engineering
It is designed to simulate how churn intelligence systems are built in real-world SaaS or
