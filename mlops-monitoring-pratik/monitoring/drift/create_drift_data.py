from pathlib import Path
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
REFERENCE_PATH = BASE_DIR / "reference_data.csv"
CURRENT_NORMAL_PATH = BASE_DIR / "current_normal_data.csv"

CURRENT_DRIFTED_PATH = BASE_DIR / "current_drifted_data.csv"

iris = load_iris(as_frame=True)

data = iris.data.copy()

data.columns = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width"
]

reference_data, current_normal_data = train_test_split(data, test_size=0.4, random_state=42)

reference_data = reference_data.reset_index(drop=True)
current_normal_data = current_normal_data.reset_index(drop = True)

current_drifted_data = current_normal_data.copy()

# sepal length dağılımı kaydır
current_drifted_data["sepal_length"] = current_drifted_data["sepal_length"] + 1.5

# sepal width dağılımını daha yüksek değerler ile kaydır
current_drifted_data["sepal_width"] = current_drifted_data["sepal_width"] + 1

# petal length drift
current_drifted_data["petal_length"] = current_drifted_data["petal_length"] + 2

# petal_width
current_drifted_data["petal_width"] = current_drifted_data["petal_width"] + 0.8

# csv olarak kaydetme
reference_data.to_csv(REFERENCE_PATH, index = False)
current_normal_data.to_csv(CURRENT_NORMAL_PATH, index = False)
current_drifted_data.to_csv(CURRENT_DRIFTED_PATH, index = False)

print(f"reference ortalamaları: \n{reference_data.mean()}")
print(f"normal current ortalamaları: \n{current_normal_data.mean()}")
print(f"current drifted ortalamaları: \n{current_drifted_data.mean()}")
