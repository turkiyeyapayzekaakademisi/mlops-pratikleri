from pathlib import Path

from shutil import copy2 

BASE_DIR = Path(__file__).resolve().parent.parent

CHAMPION_MODEL_PATH = BASE_DIR / "artifacts" / "iris_model.joblib"

CHALLENGER_MODEL_PATH = BASE_DIR / "artifacts" / "challenger_model.joblib"

CHAMPION_SCORE = 0.9
CHALLENGER_SCORE = 0.95

def promote_challenger():

    if CHALLENGER_SCORE > CHAMPION_SCORE:
        # challenger model dosyasını mevcut şampiyon modelin üzerine yaz
        copy2(CHALLENGER_MODEL_PATH, CHAMPION_MODEL_PATH)

        return

    # pipeline hatası çıkarsa
    raise SystemExit(1)

if __name__ == "__main__":
    promote_challenger()