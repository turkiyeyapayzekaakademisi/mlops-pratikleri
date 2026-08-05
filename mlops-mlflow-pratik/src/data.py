import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from src.settings import RANDOM_STATE, TEST_SIZE, VALIDATION_SIZE

def load_and_split_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    dataset = load_breast_cancer(as_frame=True)

    features = dataset.data.copy()

    # orijinal veri seti 0 = malignant 1 = benign tam tersine çevir
    target = (dataset.target == 0).astype(int)

    # split
    train_validation_features, test_features, train_validation_target, test_target = train_test_split(features, target, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=target)

    relative_validation_size = (VALIDATION_SIZE/(1-TEST_SIZE))

    train_features, validation_features, train_target, validation_target = train_test_split(train_validation_features, train_validation_target, test_size=relative_validation_size, random_state=RANDOM_STATE, stratify=train_validation_target)

    return (train_features, validation_features, test_features, train_target, validation_target, test_target)