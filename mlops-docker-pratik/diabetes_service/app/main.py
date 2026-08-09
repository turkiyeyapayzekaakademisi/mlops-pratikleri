from pathlib import Path
import pandas as pd

from joblib import load 
from fastapi import FastAPI
from pydantic import BaseModel # request ve response modelleri için

# model dosyası yolunu belirle
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "artifacts" / "diabetes_model.joblib"

# kaydedilmiş modeli yükle
model_bundle = load(MODEL_PATH)

# model bilgilerini al
model = model_bundle["model"]
feature_names = model_bundle["feature_names"]
model_version = model_bundle["model_version"]
model_r2 = model_bundle["r2_score"]

# fastapi uygulamasını oluştur
app = FastAPI(title="Diabetes Tahmini API", version=model_version)

# API'ye gönderilecek veriyi tanımla
class DiabetesInput(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float

# API'dan döenecek sonucu tanımla
class PredictionResponse(BaseModel):
    prediction: float
    model_version: str

# Ana endpoint
@app.get("/")
def root():
    return {
        "message": "diabetes api", "model_version": model_version
    }

# servis durumunu kontrol eden bir endpoint
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": model_version,
        "model_r2": model_r2
    }


# tahmin endpointi
@app.post("/predict", response_model=PredictionResponse)
def predict(data: DiabetesInput):

    # gelen veriyi df e dönüştür
    input_data = pd.DataFrame([data.model_dump()], columns=feature_names)

    # model ile tahmin yap
    prediction = model.predict(input_data)[0]

    # tahmin sonucunu döndür
    return {
        "prediction": float(prediction),
        "model_version": model_version
    }