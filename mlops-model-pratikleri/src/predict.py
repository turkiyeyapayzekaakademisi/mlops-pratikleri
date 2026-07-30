import argparse
from pathlib import Path

import pandas as pd
from joblib import load

from src.config_loader import load_config

CLASS_NAMES = {
    0: "Benign",
    1: "Malignant"
}

def validate_row_number(row_number: int, total_rows: int) -> None:
    if (row_number < 0 or row_number >= total_rows):
        raise IndexError(f"Satır numarası 0 ile {total_rows - 1} arasında olmalı.")

def main() -> None:

    parser = argparse.ArgumentParser(description=("Kaydedilen model ile test verisi üzerinde tahmin yapma"))

    parser.add_argument("--row",type=int,default=0,help=("Test veri setinde kullanılacak satır numarası"))

    arguments = parser.parse_args()
    config = load_config()

    model_path = Path(config["outputs"]["model_path"])
    test_path = Path(config["data"]["test_path"])
    target_column = (config["data"]["target_column"])

    if not model_path.exists():
        raise FileNotFoundError("model dosyası bulunamadı ",model_path)

    if not test_path.exists():
            raise FileNotFoundError("model dosyası bulunamadı ", test_path)

    dataframe = pd.read_csv(test_path)

    validate_row_number(row_number=arguments.row, total_rows=len(dataframe))

    actual_target = int(dataframe.iloc[arguments.row][target_column])

    features = dataframe.drop(columns=[target_column])

    sample = features.iloc[[arguments.row]]

    model = load(model_path)

    prediction = int(model.predict(sample)[0])

    malignant_probability = float(model.predict_proba(sample)[0, 1])

    print(f"Satır numarası: {arguments.row}")

    print(f"Gerçek sınıf: {actual_target}")
    print(f"{CLASS_NAMES[actual_target]}")

    print(f"Tahmin edilen sınıf: {prediction}")
    print(f"{CLASS_NAMES[prediction]}")

    print(f"malignant olasılığı: {malignant_probability}")

if __name__ == "__main__":
     main()
