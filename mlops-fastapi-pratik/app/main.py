from contextlib import asynccontextmanager

from fastapi import FastAPI, status

from app.model_service import model_service
from app.schemas import IrisFeatures, PredictionResponse, HealthResponse, BatchPredictionRequest, BatchPredictionResponse

from app.errors import ModelNotReadyError, PredictionError

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        model_service.load_model()
        app.state.startup_error = None
    except ModelNotReadyError as error:
        app.state.startup_error = str(error)

    yield

    model_service.unload_model()

app = FastAPI(
    title = "İris Sınıflandırma API",
    description= "İris çiçek türünü tahmin eden makine öğrenmesi API'si",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def root() -> dict[str, str]:

    return {
        "message": "Iris classification API",
        "status": "running"
    }

@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:

    bundle = model_service.get_bundle()

    return HealthResponse(
        status = "healthy",
        model_ready = model_service.is_ready,
        model_version = bundle["model_version"]
    )

# @app.post("/predict")
# def predict(payload: dict[str, float]) -> dict[str, object]:
#     return model_service.predict_one(payload)

# @app.post("/predict")
# def predict(payload: IrisFeatures) -> dict[str, object]:
#     return model_service.predict_one(payload.model_dump())

@app.post(
        "/predict", 
        response_model=PredictionResponse,
        status_code=status.HTTP_200_OK,
        summary="Tekli iris tahmini",
        description="4 tane iris featreus kullanarak tek bir çiçek türü tahmini yapar"
        )
def predict(payload: IrisFeatures) -> PredictionResponse:

    result = model_service.predict_one(payload.model_dump())
    return PredictionResponse(**result)

@app.post("/predict/batch", response_model = BatchPredictionResponse, status_code=status.HTTP_200_OK)
def predict_batch(payload: BatchPredictionRequest) -> BatchPredictionResponse:

    items = [item.model_dump() for item in payload.items]

    results = model_service.predict_batch(items)

    return BatchPredictionResponse(
        total=len(results),
        predictions=results
    )