from pathlib import Path

FOLDERS = [
    "data/raw", "data/processed",
    "notebooks",
    "src/data", "src/models", "src/training", "src/evaluation", "src/utils",
    "models",            # saved trained models
    "api",               # FastAPI backend (Phase 7)
    "dashboard",         # React + Three.js frontend (Phase 8)
    "tests",
    "configs",
    "reports/figures",
    "scripts",
]

for folder in FOLDERS:
    path = Path(folder)
    path.mkdir(parents=True, exist_ok=True)
    # Make src subfolders importable Python packages
    if folder.startswith("src"):
        (path / "__init__.py").touch()

# Keep empty folders tracked by git
for folder in ["data/raw", "data/processed", "models"]:
    (Path(folder) / ".gitkeep").touch()

print("Project structure created.")