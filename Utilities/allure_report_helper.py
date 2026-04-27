import shutil
from pathlib import Path


def zip_allure_results():
    results_dir = Path("allure-results")
    zip_path = Path("allure-results.zip")

    if not results_dir.exists():
        raise FileNotFoundError("allure-results folder not found")

    if zip_path.exists():
        zip_path.unlink()

    shutil.make_archive("allure-results", "zip", results_dir)
    return zip_path