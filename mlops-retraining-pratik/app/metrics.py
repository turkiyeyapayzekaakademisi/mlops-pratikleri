from prometheus_client import Counter, Histogram

# toplan api isteklerini say
API_REQUEST = Counter("api_requests_total", "Toplam API istek sayisi", ["method", "endpoint", "status_code"])

# hatalı api isteklerini say
API_ERRORS = Counter("api_errors_total", "toplam hatali api istek sayisi", ["method", "endpoint", "status_code"])

# api istek sürelerini ölç
API_REQUEST_DURATION = Histogram("api_request_duration_seconds", "api isteklerinin tamamlanma suresi", ["method", "endpoint"])

# modelin ürettiği tahminleri say
MODEL_PREDICTIONS = Counter("model_predictions_total", "model tahmin sayisi", ["class_name"])

# model tahmin süresini ölç
MODEL_PREDICTION_DURATION = Histogram("model_prediction_duration_seconds", "model tahmin suresi")
