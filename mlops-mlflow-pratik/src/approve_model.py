import mlflow
from mlflow import MlflowClient

from src.settings import REGISTERED_MODEL_NAME, SELECTION_METRIC, TRACKING_URL

def main() -> None:

    mlflow.set_tracking_uri(TRACKING_URL)

    client = MlflowClient()

    versions = client.search_model_versions(filter_string=(f"name='{REGISTERED_MODEL_NAME}'"))

    if not versions:
        raise RuntimeError("Registry içerisinde model versiyonu bulunamadı")

    version_results = []

    for version in versions:

        if not version.run_id: 
            continue

        run = client.get_run(version.run_id)

        metric_value = run.data.metrics.get(SELECTION_METRIC)

        if metric_value is None:
            continue

        version_results.append(
            {
                "version": (str(version.version)),
                "run_id": version.run_id,
                "metric": float(metric_value)
            }
        )

    if not version_results:
        raise RuntimeError("Seçtiğimiz metriğe sahip model versiyonu bulunamadı")

    version_results.sort(key = lambda item: item["metric"], reverse = True)

    champion = version_results[0]

    for result in version_results:

        version = result["version"]

        if version == champion["version"]:

            client.set_model_version_tag(name = REGISTERED_MODEL_NAME, version=version, key = "validation_status", value="passed")
            client.set_model_version_tag(name = REGISTERED_MODEL_NAME, version=version, key = "deployment status", value = "production_approved")
            client.set_model_version_tag(name = REGISTERED_MODEL_NAME, version=version, key = "approval_reason", value = f"Highest {SELECTION_METRIC}") 

        else:
            client.set_model_version_tag(name=REGISTERED_MODEL_NAME, version=version, key = "validation_status", value="candidate")
            client.set_model_version_tag(name = REGISTERED_MODEL_NAME, version=version, key = "deployment status", value = "npt_approved")

    client.set_registered_model_alias(name = REGISTERED_MODEL_NAME, alias="champion", version=champion["version"])

    approved_version = (
        client.get_model_version(name=REGISTERED_MODEL_NAME, version=champion["version"])
    )

    client.update_model_version(name=REGISTERED_MODEL_NAME, version=champion["version"], description="Üretim modeli")

    print("üretim onayı tamamlandı")

    print(f"Onaylanan version: \n{champion["version"]}")

if __name__ == "__main__":
    main()