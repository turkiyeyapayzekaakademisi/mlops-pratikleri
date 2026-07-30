from pathlib import Path

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = Path("data/raw/breast_cancer.csv")
TRAIN_DATA_PATH = Path("data/processed/train.csv")
VALIDATION_DATA_PATH = Path("data/processed/validation.csv")
TEST_DATA_PATH = Path("data/processed/test.csv")
TARGET_COLUMN = "target"

TEST_SIZE = 0.2
VALIDATION_SIZE = 0.2
RANDOM_STATE = 42

def create_dataframe() -> pd.DataFrame:
    dataset = load_breast_cancer(as_frame=True)

    dataframe = dataset.data.copy()

    # orijinal veri setinde malignant (kötü huylu) = 0, benign (iyi huylu) = 1
    # bu projede malignant sınıfını pozitif sınıf yapıyoruz
    dataframe[TARGET_COLUMN] = (dataset.target == 0).astype(int)

    return dataframe 

def split_dataframe(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    train_validation, test = train_test_split(dataframe, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=dataframe[TARGET_COLUMN])

    relative_validation_size = (VALIDATION_SIZE / (1 - TEST_SIZE))
    train, validation = train_test_split(train_validation, test_size=relative_validation_size, random_state=RANDOM_STATE, stratify=train_validation[TARGET_COLUMN])

    return train, validation, test

def save_dataframe(dataframe: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    dataframe.to_csv(path, index=False)

def main() -> None:

    dataframe = create_dataframe()

    train, validation, test = split_dataframe(dataframe)

    save_dataframe(dataframe, RAW_DATA_PATH)

    save_dataframe(train, TRAIN_DATA_PATH)
    save_dataframe(validation, VALIDATION_DATA_PATH)
    save_dataframe(test, TEST_DATA_PATH)

    print(f"Ham veri boyutu: {dataframe.shape}")
    print(f"Train: {len(train)}")
    print(f"validation: {len(validation)}")
    print(f"test: {len(test)}")

if __name__ == "__main__":
    main()