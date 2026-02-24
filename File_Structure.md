churn-retention-system/
│
├── app/                           # FastAPI Backend
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry
│   ├── config.py                  # BusinessConfig
│   ├── schemas.py                 # Pydantic schemas
│   ├── model_loader.py            # Load pipeline.pkl
│   ├── decision_engine.py         # Economic logic + clustering
│   ├── explainability.py          # SHAP logic (py file)
│   │
│   └── routes/
│       ├── __init__.py
│       ├── predict_single.py
│       └── predict_batch.py
│
├── models/
│   └── churn_pipeline.pkl         # Full sklearn pipeline
│
├── frontend/                      # Streamlit UI
│   ├── streamlit_app.py
│   │
│   ├── components/
│   │   ├── single_mode.py         # Form logic
│   │   ├── batch_mode.py          # CSV upload logic
│   │   ├── sliders.py             # Economic sliders
│   │   └── api_client.py          # Requests to FastAPI
│   │
│   ├──utils/
│   └── constants.py        # Required columns, default values
│   
│
├── notebooks/
│   ├── 01_model_training.ipynb
│   └── 02_decision_validation.ipynb
│
├── tests/
│   ├── test_decision_engine.py
│   └── test_api.py
│
├── Dockerfile
├── requirements.txt
├── .env
├── README.md
└── .gitignore