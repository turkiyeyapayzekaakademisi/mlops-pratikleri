import os
import time
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Request, Response
from joblib import load
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel

from app.metrics import (
    API_ERRORS,
    API_REQUEST,
    API_REQUEST_DURATION,
    MODEL_PREDICTION_DURATION,
    MODEL_PREDICTIONS,
)

# model dosya yolu
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "artifacts" / "iris_model.joblib"

# fastapi uygulaması oluştur
app = FastAPI(title="iris prediction api", version="1.0.0")


# api ya gönderilecek veri tanımlaması, request şeması
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# api den dönecek sonucun tanımlanması
class PredictionResponse(BaseModel):
    prediction: int
    class_name: str
    model_version: str


def load_model_bundle():
    return load(MODEL_PATH)

@app.middleware("http")
async def collect_api_metrics(request: Request, call_next):

    # prometheusun kendi istediğini ölçme
    if request.url.path == "/metrics":
        return await call_next(request)

    start_time = time.perf_counter()

    try: 
        response = await call_next(request)
        status_code = response.status_code
    except Exception:

        status_code = 500

        duration = time.perf_counter() - start_time

        API_REQUEST.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=status_code
        ).inc() 

        API_ERRORS.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=status_code
        ).inc() 

        API_REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)

    duration = time.perf_counter() - start_time

    # istek sayısı arttır
    API_REQUEST.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=status_code
    ).inc() 

    API_REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)

    # 4XX VE 5XX cevapları hata olarak say
    if status_code >= 400:
        API_ERRORS.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=status_code
    ).inc() 

    return response
    
@app.get("/")
def root():
    return {"message": "iris prediction api"}


@app.get("/health")
def health():
    model_bundle = load_model_bundle()

    return {
        "status": "ok",
        "environment": os.getenv("app_env", "development"),
        "model_version": model_bundle["model_version"],
        "accuracy": model_bundle["accuracy"],
    }

@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        content = generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

@app.post("/predict", response_model=PredictionResponse)
def predict(data: IrisInput):

    model_bundle = load_model_bundle()

    model = model_bundle["model"]
    feature_names = model_bundle["feature_names"]
    target_names = model_bundle["target_names"]

    # model girdisi oluştur
    input_data = pd.DataFrame(
        [[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]],
        columns=feature_names,
    )

    prediction_start = time.perf_counter()

    # tahmin yapma
    prediction = int(model.predict(input_data)[0])

    prediction_duration = time.perf_counter() - prediction_start

    class_name = target_names[prediction]

    # tahmin süresini kaydet
    MODEL_PREDICTION_DURATION.observe(prediction_duration)

    # tahmin edilen sınıfı say
    MODEL_PREDICTIONS.labels(
        class_name = class_name
    ).inc()
    
    return {
        "prediction": prediction,
        "class_name": class_name,
        "model_version": model_bundle["model_version"],
    }
