from datetime import datetime

from namozvaqti.cache import load_month
from namozvaqti.format import build_waybar_output


def main():
    now = datetime.now()
    cache = load_month(now.year, now.month)
    print(build_waybar_output(cache))


if __name__ == "__main__":
    main()
