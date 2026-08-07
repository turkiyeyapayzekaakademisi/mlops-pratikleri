from pydantic import BaseModel, ConfigDict, Field
from typing import Any

class IrisFeatures(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "sepal_length_cm": 5.1,
                "sepal_width_cm": 3.5,
                "petal_length_cm": 1.4,
                "petal_width_cm": 0.5
            }
        }
    )

    sepal_length_cm: float = Field(
        gt = 0, # greater than
        le = 10, # less than veya equal
        description="sepal_length_cm",
        examples=[5.1]
    )
    sepal_width_cm: float = Field(
        gt = 0, le = 10, description="sepal_width_cm", examples=[3.5]
    )
    petal_length_cm: float = Field(
        gt = 0, le = 10, description="petal_length_cm", examples=[3.5]
    )
    petal_width_cm: float = Field(
        gt = 0, le = 10, description="petal_width_cm", examples=[3.5]
    )

class PredictionResponse(BaseModel):

    model_version: str
    predicted_class: int
    predicted_label: str
    probabilities: dict[str, float]

class HealthResponse(BaseModel):
    status: str
    model_ready: bool
    model_version: str | None = None


class BatchPredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[IrisFeatures] = Field(
        min_length=1,
        max_length=100, 
        description="Tahmin edilecek iris kayıtları"
    )

class BatchPredictionItem(PredictionResponse):
    input_index: int

class BatchPredictionResponse(BaseModel):
    total: int
    predictions: list[BatchPredictionItem]

class ErrorResponse(BaseModel):

    error: str
    message: str
    details: list[dict[str, Any]] | None = None