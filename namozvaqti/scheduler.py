import time
from datetime import datetime

from namozvaqti.notify import notify
from namozvaqti.service import get_next_prayer


def run():
    last_notified = None

    while True:
        now = datetime.now()

        name, prayer = get_next_prayer(now)
        prayer_time = datetime.fromtimestamp(prayer["timestamp"])

        wait_seconds = max(0, (prayer_time - now).total_seconds())

        if wait_seconds > 0:
            time.sleep(wait_seconds)

        # Prevent duplicate notifications
        if last_notified != name:
            notify(
                title=f"{name} time",
                message=prayer_time.strftime("%H:%M"),
            )
            last_notified = name

        # small buffer to avoid re-trigger
        time.sleep(60)


if __name__ == "__main__":
    run()
