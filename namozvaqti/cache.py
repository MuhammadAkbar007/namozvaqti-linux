import json
from datetime import datetime
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


def load_today() -> dict:
    now = datetime.now()
    data = load_month(now.year, now.month)

    if data is None:
        raise RuntimeError("Monthly cache not found")

    today_key = now.strftime("%Y-%m-%d")

    if today_key not in data:
        raise RuntimeError("Today's data not found")

    return data[today_key]


def load_day(date: datetime) -> dict:
    data = load_month(date.year, date.month)

    if data is None:
        raise RuntimeError("Monthly cache not found")

    key = date.strftime("%Y-%m-%d")

    if key not in data:
        raise RuntimeError(f"No data for {key}")

    return data[key]
