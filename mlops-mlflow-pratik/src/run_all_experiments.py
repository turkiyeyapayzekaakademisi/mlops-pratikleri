from typing import Any
from src.run_experiment import run_experiment

EXPERIMENT_CONFIGURATIONS: list[
    dict[str, Any]
] = [
    {
        "run_name": "logistic_regression-c0-1",
        "model_name": "logistic_regression",
        "parameters": {
            "C": 0.1,
            "max_iter": 1000,
            "solver": "lbfgs"
        } 
    },
    {
        "run_name": "logistic_regression-c1",
        "model_name": "logistic_regression",
        "parameters": {
            "C": 1,
            "max_iter": 1000,
            "solver": "lbfgs"
        } 
    },
    {
        "run_name": "logistic_regression-c10",
        "model_name": "logistic_regression",
        "parameters": {
            "C": 10,
            "max_iter": 1000,
            "solver": "lbfgs"
        } 
    },
    {
        "run_name": "random-forest-100",
        "model_name": "random_forest",
        "parameters": {
            "n_estimators": 100,
            "max_depth": 3,
            "min_samples_split": 2
        }
    },
    {
        "run_name": "random-forest-300",
        "model_name": "random_forest",
        "parameters": {
            "n_estimators": 300,
            "max_depth": 3,
            "min_samples_split": 2
        }
    },
    {
        "run_name": "svm-c1",
        "model_name": "svm",
        "parameters": {
            "C": 1,
            "kernel": "rbf",
            "gamma": "scale"
        }
    },
    {
        "run_name": "svm-c10",
        "model_name": "svm",
        "parameters": {
            "C": 10,
            "kernel": "rbf",
            "gamma": "scale"
        }
    }
]

def main() -> None:

    run_ids = []

    for index, configuration in enumerate(EXPERIMENT_CONFIGURATIONS, start=1):

        print(f"Deney: {index}")
        print(f"Run: {configuration["run_name"]}")

        run_id = run_experiment(run_name=configuration["run_name"], model_name=configuration["model_name"], model_parameters=configuration["parameters"])
        run_ids.append(run_id)
        
    print("Bütün deneyler tamamlandı")
    print(f"Toplam run sayısı: {len(run_ids)}")

    for run_id in run_ids:
        print(run_id)

if __name__ == "__main__":
    main()