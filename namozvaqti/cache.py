import json
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "namozvaqti"


def ensure_cache_dir():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def save_month(year: int, month: int, data: dict):
    ensure_cache_dir()

    filename = f"{year}-{month:02d}.json"
    path = CACHE_DIR / filename

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_month(year: int, month: int) -> dict | None:
    filename = f"{year}-{month:02d}.json"
    path = CACHE_DIR / filename

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)
