from pathlib import Path
from typing import Any

from joblib import load
import pandas as pd

from app.errors import ModelNotReadyError, PredictionError

MODEL_PATH = Path("artifacts/iris_classifier.joblib")

class ModelService:

    def __init__(self) -> None:

        self._bundle: (
            dict[str, Any] | None
        ) = None

    @property
    def is_ready(self) -> bool:
        return self._bundle is not None

    def load_model(self) -> None:

        if not MODEL_PATH.exists():
            raise ModelNotReadyError(f"Model dosyası bulunamadı: {MODEL_PATH}")

        try:
            bundle = load(MODEL_PATH)
        except Exception as error:
            raise ModelNotReadyError("Model dosyası yüklemedi") from error
        
        required_keys = {
            "model",
            "feature_names",
            "class_names",
            "model_version"
        }

        missing_keys = (required_keys - bundle.keys())

        if missing_keys: 
            raise ModelNotReadyError(f"Model paketinde eksik alanlar var: {sorted(missing_keys)}")

        self._bundle = bundle

    def unload_model(self) -> None:
        self._bundle = None

    def get_bundle(self) -> dict[str, Any]:
        if self._bundle is None:
            raise ModelNotReadyError("Model henüz yüklenmedi")

        return self._bundle

    def predict_one(self, features: dict[str, float]) -> dict[str, object]:

        bundle = self.get_bundle()

        feature_frame = pd.DataFrame([features], columns = bundle["feature_names"])

        model = bundle["model"]

        try:
            predicted_class = int(model.predict(feature_frame)[0])

            probabilities = model.predict_proba(feature_frame)[0]
        except Exception as error:
            raise PredictionError("Model tahmini sırasında beklenmeyen bir hata oluştu") from error
        
        class_names = bundle["class_names"]

        probability_mapping = {
            str(class_name): round(float(probability), 4) for class_name, probability in zip(class_names, probabilities, strict=True)
        }

        return {
            "model_version": bundle["model_version"],
            "predicted_class": predicted_class,
            "predicted_label": str(class_names[predicted_class]),
            "probabilities": probability_mapping
        }

    def predict_batch(self, items: list[dict[str, float]]) -> list[dict[str, object]]:
        bundle = self.get_bundle()

        feature_frame = pd.DataFrame(items, columns=bundle["feature_names"])

        model = bundle["model"]

        predicted_classes = model.predict(feature_frame)

        probability_rows = model.predict_proba(feature_frame)

        class_names = bundle["class_names"]

        result = []

        for input_index, predicted_class, probabilities in zip(range(len(items)), predicted_classes, probability_rows, strict=True):
            predicted_class = int(predicted_class)

            probability_mapping = {
                        str(class_name): round(float(probability), 4) for class_name, probability in zip(class_names, probabilities, strict=True)
                    }

            result.append(
                {
                    "input_index": input_index,
                    "model_version": bundle["model_version"],
                    "predicted_class": predicted_class,
                    "predicted_label": class_names[predicted_class],
                    "probabilities": probability_mapping
                }
            ) 
        return result
                    
  
model_service = ModelService()

