from datetime import datetime, timedelta

REGION = "namangan"


def ensure_month(year: int, month: int):
    from namozvaqti.cache import load_month, save_month
    from namozvaqti.fetch import fetch_month
    from namozvaqti.parse import parse_month

    data = load_month(year, month)

    if data is not None:
        return data

    # fetch → parse → save
    html = fetch_month(REGION, month)
    parsed = parse_month(html, year, month)

    save_month(year, month, parsed)

    return parsed


def get_day(date: datetime) -> dict:
    month_data = ensure_month(date.year, date.month)

    key = date.strftime("%Y-%m-%d")

    if key not in month_data:
        raise RuntimeError(f"No data for {key}")

    return month_data[key]


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
