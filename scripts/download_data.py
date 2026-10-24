import shutil
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

URL = ("https://phm-datasets.s3.amazonaws.com/NASA/"
       "6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip")

RAW_DIR = Path("data/raw")
ZIP_PATH = RAW_DIR / "cmapss_download.zip"
TMP_DIR = RAW_DIR / "_extract_tmp"

EXPECTED = [f"{kind}_FD00{i}.txt"
            for i in range(1, 5)
            for kind in ("train", "test", "RUL")]


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(dest, "wb") as f, tqdm(
            total=total, unit="B", unit_scale=True, desc="Downloading"
        ) as bar:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                f.write(chunk)
                bar.update(len(chunk))


def extract_all(zip_path: Path, out_dir: Path) -> None:
    """Extract a zip, then keep extracting any zips found inside it."""
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(out_dir)

    while True:
        nested_zips = list(out_dir.rglob("*.zip"))
        if not nested_zips:
            break
        for nested in nested_zips:
            with zipfile.ZipFile(nested) as z:
                z.extractall(nested.parent)
            nested.unlink()   # delete right after extracting, so it's never found again


def main() -> None:
    if all((RAW_DIR / name).exists() for name in EXPECTED):
        print("Dataset already present. Nothing to do.")
        return

    print("Downloading C-MAPSS dataset...")
    download(URL, ZIP_PATH)

    print("Extracting...")
    TMP_DIR.mkdir(exist_ok=True)
    extract_all(ZIP_PATH, TMP_DIR)

    # Move the data files (and docs) to data/raw, wherever they ended up
    for path in TMP_DIR.rglob("*"):
        if path.is_file() and (path.name in EXPECTED
                               or path.suffix.lower() in {".pdf"}
                               or path.name.lower() == "readme.txt"):
            shutil.move(str(path), RAW_DIR / path.name)

    shutil.rmtree(TMP_DIR, ignore_errors=True)
    ZIP_PATH.unlink(missing_ok=True)

    missing = [n for n in EXPECTED if not (RAW_DIR / n).exists()]
    if missing:
        print("WARNING, missing files:", missing)
    else:
        print("Done. All 12 data files are in data/raw/")


if __name__ == "__main__":
    main()