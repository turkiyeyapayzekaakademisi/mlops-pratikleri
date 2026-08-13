from pathlib import Path
import os
import pandas as pd
from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel

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

    # tahmin yapma
    prediction = int(model.predict(input_data)[0])

    return {
        "prediction": prediction,
        "class_name": target_names[prediction],
        "model_version": model_bundle["model_version"],
    }
