from pathlib import Path
import pandas as pd

def load_split(path: Path, target_column: str) -> tuple[pd.DataFrame, pd.Series]:

    if not path.exists():
        raise FileNotFoundError("Veri dosyası bulunamadı")

    dataframe = pd.read_csv(path)

    if target_column not in dataframe.columns:
        raise ValueError("Hedef sütun bulunamadı.")

    features = dataframe.drop(columns=[target_column])
    target = dataframe[target_column]

    return features, target

