# Deployment: Operational Guide

This document provides instructions for deploying the Churn Intelligence Platform in production and staging environments.

## Deployment Options

### 1. Docker Compose (Recommended)
The simplest way to run the full stack (Backend + Frontend + Monitoring).

```bash
# Build and start all services
docker-compose up --build -d
```

### 2. Manual Python Setup
If you prefer to run services individually without Docker:

```bash
# Backend
pip install -r requirements.txt
uvicorn app.main:app --port 8000

# Frontend
streamlit run frontend/streamlit_app.py --server.port 8501
```

---

## Configuration

The system is configured via environment variables. Create a `.env` file in the root directory:

| Variable | Description | Default |
| :--- | :--- | :--- |
| `MODEL_PATH` | Path to the `.pkl` pipeline file. | `models/churn_pipeline.pkl` |
| `MONITORING_DB_PATH` | Path to the SQLite DB (Inside container). | `/app/data/monitoring.db` |
| `PORT` | API Port. | `8000` |
| `BACKEND_URL` | Used by the Frontend to find the API. | `http://localhost:8000` |

---

## Data Persistence
> [!IMPORTANT]
> To ensure you do not lose prediction monitoring data during updates, always use the Docker volume defined in `docker-compose.yml`.

- **Volume Name**: `monitor_data`
- **Mount Point**: `/app/data`

## Staging & Production
- **Scaling**: The Backend is stateless and can be scaled horizontally behind a load balancer (e.g., Nginx, Traefik).
- **Inference**: For high-volume batch jobs, consider increasing the Pydantic worker count in `uvicorn` using `--workers N`.
