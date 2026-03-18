from datetime import datetime


def get_today(cache: dict):
    today = datetime.now().strftime("%Y-%m-%d")
    return cache.get(today)


def get_next_prayer(day_data: dict, now_ts: int):
    ordered = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]

    for name in ordered:
        if day_data[name]["timestamp"] > now_ts:
            return name, day_data[name]

    # Edge case: after isha → next day's fajr
    return "fajr", None  # handle properly later


def get_next_prayer_with_rollover(cache, today_data, now_ts):
    name, prayer = get_next_prayer(today_data, now_ts)

    if prayer is not None:
        return name, prayer

    # after isha → load tomorrow
    from datetime import datetime, timedelta

    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow_data = cache.get(tomorrow)

    return "fajr", tomorrow_data["fajr"]
