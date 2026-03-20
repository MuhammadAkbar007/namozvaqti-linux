import json
from datetime import datetime


def time_remaining(target_ts: int, now_ts: int):
    diff = max(0, int(target_ts - now_ts))

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


def build_waybar_output():
    try:
        from namozvaqti.service import get_day, get_next_prayer

        now = datetime.now()
        now_ts = int(now.timestamp())

        today_data = get_day(now)
        name, prayer = get_next_prayer(now)

        text = format_text(name, prayer, now_ts)
        tooltip = format_tooltip(today_data)

        return json.dumps({"text": text, "tooltip": tooltip})
    except Exception as e:
        return json.dumps(
            {
                "text": "󰔟 Loading...",
                "tooltip": str(e),
            }
        )
