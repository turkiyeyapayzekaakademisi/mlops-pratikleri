from pathlib import Path
import pandas as pd
from evidently import Dataset
from evidently import DataDefinition
from evidently import Report
from evidently.presets import DataDriftPreset
from evidently.ui.workspace import Workspace

BASE_DIR = Path(__file__).resolve().parents[2]

# data drift csv dosyaları yolu
DRIFT_DIR = BASE_DIR / "monitoring" / "drift"
WORKSPACE_PATH = BASE_DIR / "evidently_workspace"

REFERENCE_PATH = DRIFT_DIR / "reference_data.csv"
CURRENT_NORMAL_PATH = DRIFT_DIR / "current_normal_data.csv"
CURRECT_DRIFTED_PATH = DRIFT_DIR / "current_drifted_data.csv"

reference_df = pd.read_csv(REFERENCE_PATH)
current_normal_df = pd.read_csv(CURRENT_NORMAL_PATH)
current_drifted_df = pd.read_csv(CURRECT_DRIFTED_PATH)

# evidently'ye dört feature'ın sayısal olduğunu bildir
data_definition = DataDefinition(numerical_columns=["sepal_length", "sepal_width", "petal_length", "petal_width"])

# pandas to evidently dataset
reference_data = Dataset.from_pandas(reference_df, data_definition=data_definition)
current_normal_data = Dataset.from_pandas(current_normal_df, data_definition=data_definition)
current_drifted_data = Dataset.from_pandas(current_drifted_df, data_definition=data_definition)

# tüm feature'lar için data drift analizi yapacak olan evidently report oluştur
report = Report([DataDriftPreset()])

normal_result = report.run(
    current_data=current_normal_data,
    reference_data=reference_data
)

drifted_result = report.run(
    current_data=current_drifted_data,
    reference_data=reference_data
)

workspace= Workspace.create(WORKSPACE_PATH)

projects = workspace.search_project("Iris Data Drift Monitoring")

if projects:
    project = projects[0]
else:
    project = workspace.create_project("Iris Data Drift Monitoring")

    project.description = "Iris modeli için data drift"

    project.save()

workspace.add_run(project.id, normal_result, include_data=False)
workspace.add_run(project.id, drifted_result, include_data=False)

print(f"Project: {project.name}")
print(f"Workspace: {WORKSPACE_PATH}")
