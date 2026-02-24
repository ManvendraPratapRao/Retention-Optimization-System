from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import predict_single, predict_batch, model_info

app = FastAPI(
    title="Churn Retention System API",
    description="ML-powered churn prediction with economic decision engine",
    version="1.0.0"
)

# -----------------------------
# CORS (needed for Streamlit frontend)
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(predict_single.router)
app.include_router(predict_batch.router)
app.include_router(model_info.router)

# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}