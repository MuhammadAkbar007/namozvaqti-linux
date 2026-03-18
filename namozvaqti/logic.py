from datetime import datetime, timedelta

from namozvaqti.cache import load_day

PRAYER_ORDER = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]


def parse_time(today: dict, key: str) -> datetime:
    now = datetime.now()
    time_str = today[key]  # "16:36"

    hour, minute = map(int, time_str.split(":"))

    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)


def get_next_prayer(now: datetime):
    today = load_day(now)

    now_ts = int(now.timestamp())

    # 1️⃣ Try today
    for name in PRAYER_ORDER:
        prayer_ts = today[name]["timestamp"]

        if prayer_ts > now_ts:
            prayer_time = datetime.fromtimestamp(prayer_ts)
            return name.capitalize(), prayer_time

    # 2️⃣ Fallback → tomorrow fajr
    tomorrow = now + timedelta(days=1)
    tomorrow_data = load_day(tomorrow)

    fajr_ts = tomorrow_data["fajr"]["timestamp"]

    return "Fajr", datetime.fromtimestamp(fajr_ts)
