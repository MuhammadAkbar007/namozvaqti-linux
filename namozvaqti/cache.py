import json
from datetime import datetime
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "namozvaqti"


def ensure_cache_dir():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _day_key(date) -> str:
    # accepts a datetime or an already-formatted "YYYY-MM-DD" string
    return date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)


def save_day(date, day: dict):
    """Cache one day's enriched prayer dict at ~/.cache/namozvaqti/YYYY-MM-DD.json.

    praytime.uz only serves *today*, so the cache is per-day rather than the old
    per-month file the (now dead) namozvaqti.uz scraper used.
    """
    ensure_cache_dir()
    path = CACHE_DIR / f"{_day_key(date)}.json"

    with open(path, "w") as f:
        json.dump(day, f, indent=2)


def load_day(date) -> dict | None:
    path = CACHE_DIR / f"{_day_key(date)}.json"

    if not path.exists():
        return None

    with open(path) as f:
        return json.load(f)


def load_today() -> dict | None:
    return load_day(datetime.now())


def load_latest_before(date) -> tuple[str, dict] | None:
    """Return (date_key, day) for the most recent cached day *before* ``date``.

    Used as the offline/stale fallback when today can't be fetched. Filenames are
    ``YYYY-MM-DD.json`` so a lexical sort is chronological.
    """
    if not CACHE_DIR.exists():
        return None

    key = _day_key(date)
    candidates = sorted(p for p in CACHE_DIR.glob("*.json") if p.stem < key)
    if not candidates:
        return None

    latest = candidates[-1]
    with open(latest) as f:
        return latest.stem, json.load(f)
