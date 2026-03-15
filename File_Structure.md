churn-retention-system/
│
├── app/                           # FastAPI Backend
│   ├── core/
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
├── artifacts/
│   ├── churn_model_calibrated.pkl
│   └── preprocessor.pkl
│
├── models/
│   ├── churn_pipeline.pkl        # Full sklearn pipeline
│   ├── background_sample.csv
│   ├── metadata.json
│   └── preprocessor.pkl
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
│   ├── decision_engine.ipynb
│   ├── EDA.ipynb
│   ├── Feature Engineering.ipynb
│   ├── Model_train.ipynb
│   ├── Problem_Framing.ipynb
│   ├── shap_file_test.ipynb
│   └── sample.ipynb
│
├── docs/
│   ├── architecture.md
│   ├── modeling.md
│   ├── api_contract.md
│   ├── deployment.md
│   ├── decision_engine.md
│   └── explainability.md
│
├── diagrams/
│   ├── system_architecture.png
│   ├── model_pipeline.png
│   ├── decision_flow.png
│   └── api_flow.png
│
├── tests/
│   ├── test_decision_engine.py
│   └── test_api.py
│
├── venv/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.frontend
├── requirements.txt
└── README.md
