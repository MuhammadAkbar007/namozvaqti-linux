from datetime import datetime, timedelta

from namozvaqti.cache import load_month

REGION = "namangan"


def ensure_month(year: int, month: int):
    from namozvaqti.cache import load_month, save_month
    from namozvaqti.fetch import fetch_month
    from namozvaqti.parse import parse_month
    from namozvaqti.transform import enrich_with_timestamps

    data = load_month(year, month)

    if data is not None:
        return data

    try:
        # fetch → parse → save
        html = fetch_month(REGION, month)
        parsed = parse_month(html, year, month)
        enriched = enrich_with_timestamps(parsed)

        save_month(year, month, enriched)
        return enriched

    except Exception as e:
        print(f"[Cache] Failed to fetch {year}-{month:02d}: {e}")

        # ❗ fallback strategy
        previous = load_month(year, month - 1)

        if previous:
            print("[Cache] Using previous month as fallback")
            return previous

        raise RuntimeError("No data available (offline + no cache)")  # noqa: B904


def get_day(date: datetime) -> dict:
    from namozvaqti.background import ensure_month_async

    data = load_month(date.year, date.month)

    if data is None:
        ensure_month_async(date.year, date.month)
        raise RuntimeError("Cache missing (fetching in background)")

    key = date.strftime("%Y-%m-%d")

    if key not in data:
        raise RuntimeError(f"No data for {key}")

    return data[key]


def get_next_prayer(now: datetime):
    ordered = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]

    now_ts = int(now.timestamp())

    today_data = get_day(now)

    # 1️⃣ try today
    for name in ordered:
        if today_data[name]["timestamp"] > now_ts:
            return name, today_data[name]

    # 2️⃣ fallback → tomorrow fajr
    tomorrow = now + timedelta(days=1)
    tomorrow_data = get_day(tomorrow)

    return "fajr", tomorrow_data["fajr"]
