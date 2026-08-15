from importlib.util import find_spec  # python paketlerini kontrol etmek için
from pathlib import Path

import pytest

# kontrol edilecek proje ve klasörler
PROJECT_DIRECTORIES = ["app", "training", "tests", "artifacts"]

# kontrol edilecek temel python paketleri
REQUIRED_PACKAGES = ["pandas", "sklearn", "joblib", "fastapi"]


@pytest.mark.parametrize("directory", PROJECT_DIRECTORIES)
def test_project_directory_exists(directory):
    assert Path(directory).is_dir()


@pytest.mark.parametrize("package_name", REQUIRED_PACKAGES)
def test_required_package_is_installed(package_name):
    assert find_spec(package_name) is not None
