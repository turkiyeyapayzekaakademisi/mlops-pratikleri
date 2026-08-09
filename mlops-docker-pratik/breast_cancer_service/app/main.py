from pathlib import Path
import pandas as pd
from joblib import load
from fastapi import FastAPI
from pydantic import BaseModel 

# model dosyasını oku
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "artifacts" / "breast_cancer_model.joblib"

# model paketini yükle
model_bundle = load(MODEL_PATH)

# model bilgilerini al
model = model_bundle["model"]
feature_names = model_bundle["feature_names"]
target_names = model_bundle["target_names"]
model_version = model_bundle["model_version"]
model_accuracy = model_bundle["accuracy"]

# fastapi uygulaması oluştur
app = FastAPI()

# api ye gönderilecek veriyi tanımla
class BreastCancerInput(BaseModel): 
    mean_radius: float 
    mean_texture: float 
    mean_perimeter: float 
    mean_area: float 
    mean_smoothness: float 
    mean_compactness: float 
    mean_concavity: float 
    mean_concave_points: float 
    mean_symmetry: float 
    mean_fractal_dimension: float 
    radius_error: float 
    texture_error: float 
    perimeter_error: float 
    area_error: float 
    smoothness_error: float 
    compactness_error: float 
    concavity_error: float 
    concave_points_error: float 
    symmetry_error: float 
    fractal_dimension_error: float 
    worst_radius: float 
    worst_texture: float 
    worst_perimeter: float 
    worst_area: float 
    worst_smoothness: float 
    worst_compactness: float 
    worst_concavity: float 
    worst_concave_points: float 
    worst_symmetry: float 
    worst_fractal_dimension: float

# ana endpoint
@app.get("/")
def root():
    return{
        "message": "breast cancer api",
        "model_version": model_version
    }

# health endpoint
@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_version": model_version,
        "accuracy": model_accuracy
    }

# tahmin endpoint oluştur
@app.post("/predict")
def predict(data: BreastCancerInput):

    input_dict = data.model_dump()

    input_dict = {
        key.replace("_", " "): value
        for key, value in input_dict.items()
    }   

    # model girdisini oluştur
    input_data = pd.DataFrame([input_dict], columns=feature_names)

    prediction = int(model.predict(input_data)[0])

    # sınıf ismi belirle
    class_name = target_names[prediction]

    return {
        "prediction": prediction,
        "class_name": class_name,
        "model_version": model_version
    }