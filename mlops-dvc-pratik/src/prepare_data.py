from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = Path("data/raw/breast_cancer.csv")
PROCESSED_DATA_DIR = Path("data/processed")
PARAMS_PATH = Path("params.yaml")

def load_parameters() -> dict:
    with PARAMS_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def split_data(dataframe: pd.DataFrame, test_size: float, validation_size: float, random_state: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if test_size <= 0 or validation_size <= 0:
        raise ValueError("test ve validasyon oranları sıfırdan büyük olmalı")

    if test_size + validation_size >=1:
        raise ValueError("Test ve validasyon oranlarının toplamı 1 den küçük olmalı")

    train_validasyon, test = train_test_split(dataframe, test_size=test_size, random_state=random_state, stratify=dataframe["target"])

    relative_validation_size = validation_size / (1 - test_size)
    train, validation = train_test_split(train_validasyon, test_size=relative_validation_size, random_state=random_state, stratify=train_validasyon["target"])

    return train, validation, test

def save_data(train: pd.DataFrame, validation: pd.DataFrame, test: pd.DataFrame) -> None:

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    train.to_csv(PROCESSED_DATA_DIR / "train.csv", index=False)
    validation.to_csv(PROCESSED_DATA_DIR / "validation.csv", index=False)
    test.to_csv(PROCESSED_DATA_DIR / "test.csv", index=False)

def main() -> None:

    parameters = load_parameters()
    split_parameters = parameters["split"]

    dataframe = pd.read_csv(RAW_DATA_PATH)

    train, validation, test = split_data(
        dataframe = dataframe, 
        test_size = split_parameters["test_size"], 
        validation_size = split_parameters["validation_size"], 
        random_state = split_parameters["random_state"])

    save_data(train, validation, test)

    print(f"Train kayıt sayısı: {len(train)}")
    print(f"Validation kayıt sayısı: {len(validation)}")
    print(f"Test kayıt sayısı: {len(test)}")

if __name__ == "__main__":
    main()