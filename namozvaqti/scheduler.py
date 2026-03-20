import subprocess
import time
from datetime import datetime

from namozvaqti.notify import notify
from namozvaqti.service import get_next_prayer


def send_waybar_signal():
    try:
        subprocess.run(["pkill", "-RTMIN+8", "waybar"], check=False)
    except Exception as e:
        print(f"[Waybar] Signal failed: {e}")


def run():
    last_notified_ts = None

    while True:
        now = datetime.now()

        try:
            name, prayer = get_next_prayer(now)
            prayer_time = datetime.fromtimestamp(prayer["timestamp"])
        except Exception as e:
            print(f"[Scheduler] Failed to get prayer time: {e}")
            time.sleep(60)
            continue

        wait_seconds = max(0, (prayer_time - now).total_seconds())

        if wait_seconds > 0:
            time.sleep(wait_seconds)

        # Prevent duplicate notifications
        if last_notified_ts != prayer["timestamp"]:
            notify(
                title=f"{name} time",
                message=prayer_time.strftime("%H:%M"),
            )
            send_waybar_signal()
            last_notified_ts = prayer["timestamp"]

        # small buffer to avoid re-trigger
        time.sleep(5)


if __name__ == "__main__":
    run()
