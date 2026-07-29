from pathlib import Path

from sklearn.datasets import load_breast_cancer

OUTPUT_PATH = Path("data/raw/breast_cancer.csv")

def main() -> None:
    dataset = load_breast_cancer(as_frame=True)

    dataframe = dataset.frame.copy()

    dataframe.insert(
        loc = 0, 
        column = "record_id",
        value = range(1, len(dataframe) + 1)
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(OUTPUT_PATH, index = False)

    print(f"Veri seti oluşturuldu: {OUTPUT_PATH}")
    print(f"Satır sayısı: {dataframe.shape[0]}")
    print(f"Sütun sayısı: {dataframe.shape[1]}")

if __name__ == "__main__":
    main()