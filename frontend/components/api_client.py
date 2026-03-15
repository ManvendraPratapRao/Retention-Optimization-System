import requests
import os

BASE_URL = os.getenv(
    "BACKEND_URL",
    "http://localhost:8000"
)

def predict_single(payload):
    response = requests.post(f"{BASE_URL}/predict-single", json=payload)
    return response


def predict_batch(file, business_config):
    files = {"file": file}
    data = business_config

    response = requests.post(
        f"{BASE_URL}/predict-batch",
        files=files,
        data=data
    )

    return response