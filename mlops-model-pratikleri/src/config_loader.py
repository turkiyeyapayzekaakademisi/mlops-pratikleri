from pathlib import Path

import yaml

DEFAULT_CONFIG_PATH = Path("config/config.yaml")

def load_config(path: Path = DEFAULT_CONFIG_PATH) -> dict:

    if not path.exists():
        raise FileNotFoundError("Config dosyası bulunamadı")

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError("Config dosyası boş olamaz")

    return config