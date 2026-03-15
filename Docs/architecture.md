# System Architecture: Churn Intelligence Platform

This document outlines the high-level architecture of the Churn Prediction & Retention Optimization system.

## High-Level Overview

The system is designed as a modular, containerized ML application that bridges the gap between raw predictive modeling and business strategic action.

```mermaid
graph TD
    subgraph Client_Layer [Frontend Layer]
        UI[Streamlit Dashboard]
        API_C[API Client]
    end

    subgraph API_Layer [Backend Layer]
        FA[FastAPI Gateway]
        ML_L[Model Loader]
        DE[Economic Decision Engine]
        SHAP[SHAP Explainer]
        MON[Monitoring Service]
    end

    subgraph Data_Persistence [Storage Layer]
        DB[(SQLite Monitoring DB)]
        ARTIFACTS[[ML Pipeline Artifacts]]
    end

    %% Interactions
    UI --> API_C
    API_C -->|POST /predict| FA
    FA --> ML_L
    ML_L --> ARTIFACTS
    FA --> DE
    FA --> SHAP
    FA --> MON
    MON -->|Log Prediction| DB
    UI -->|GET /metrics| FA
```

## Component Breakdown

### 1. Frontend Layer (Streamlit)
- **Dashboard**: Provides a premium UI for single and batch predictions.
- **Visualizations**: Uses Plotly for interactive risk analysis and system monitoring.
- **Dynamic Recommendations**: Translates ML probabilities into human-readable business advice.

### 2. Backend Layer (FastAPI)
- **FastAPI Gateway**: Handles request validation, routing, and error management.
- **Model Loader**: Singleton service that manages the lifecycle of the Scikit-Learn/XGBoost pipeline and SHAP assets.
- **Economic Decision Engine**: Decoupled logic that applies business thresholds (ROI, BRV) to model outputs.
- **SHAP Explainer**: Generates local feature importance for every individual prediction request.
- **Monitoring Service**: Tracks prediction distribution and feature drift in real-time.

### 3. Data & Storage
- **ML Artifacts**: Pickle files containing the calibrated pipeline and preprocessors.
- **Monitoring DB**: SQLite database used for persistent tracking of every prediction event and its economic outcome.

## Technical Stack
- **Languages**: Python 3.11
- **ML Frameworks**: Scikit-Learn, XGBoost, SHAP
- **API**: FastAPI, Pydantic, Uvicorn
- **UI**: Streamlit, Plotly
- **Ops**: Docker, Docker Compose, SQLite
