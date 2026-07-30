from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def build_preprocessor(imputer_strategy: str = "median") -> Pipeline:

    return Pipeline(
        steps = [
            (
                "imputer",
                SimpleImputer(strategy=imputer_strategy), # eksik veri doldurma
            ),
            (
                "scaler",
                StandardScaler(), # ölçeklendirme
            )
        ]
    )