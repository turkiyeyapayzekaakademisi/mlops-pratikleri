import mlflow
import mlflow.pyfunc

from src.data import load_and_split_data
from src.settings import REGISTERED_MODEL_NAME, TRACKING_URL

def main() -> None:

    mlflow.set_tracking_uri(TRACKING_URL)

    model_uri = (
        f"models:/{REGISTERED_MODEL_NAME}@champion"
    )

    model = mlflow.pyfunc.load_model(model_uri=model_uri)

    train_features, validation_features, test_features, train_target, validation_target, test_target = load_and_split_data()

    sample = test_features.head(5)

    predictions = model.predict(sample)

    print(f"Model uri: {model_uri}")
    print("Tahminler: ")

    for index, prediction in enumerate(predictions, start=1):

        class_name = ("Malignant" if int(prediction) == 1 else "Benign")

        print(f"{index}. tahmin: {int(prediction)} -- {class_name}")

if __name__ == "__main__":
    main()

