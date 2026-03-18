import json
from datetime import datetime

from namozvaqti.service import get_next_prayer_with_rollover, get_today


def time_remaining(target_ts: int, now_ts: int):
    diff = int(target_ts - now_ts)

    hours = diff // 3600
    minutes = (diff % 3600) // 60

    return f"{hours}h {minutes}m"


def format_text(name, prayer, now_ts):
    remaining = time_remaining(prayer["timestamp"], now_ts)
    return f"  {name.capitalize()} {prayer['time']} (in {remaining})"


def format_tooltip(day_data):
    order = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]

    lines = []
    for name in order:
        time = day_data[name]["time"]
        lines.append(f"{name.capitalize():<8} {time}")

    return "\n".join(lines)


def build_waybar_output(cache):
    now_ts = int(datetime.now().timestamp())

    today_data = get_today(cache)
    name, prayer = get_next_prayer_with_rollover(cache, today_data, now_ts)

    text = format_text(name, prayer, now_ts)
    tooltip = format_tooltip(today_data)

    return json.dumps({"text": text, "tooltip": tooltip})
