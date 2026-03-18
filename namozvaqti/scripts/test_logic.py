from datetime import datetime

from namozvaqti.cache import load_today
from namozvaqti.logic import get_next_prayer

now = datetime.now()
today = load_today()

name, time = get_next_prayer(now, today)

print("Now:", now)
print("Next prayer:", name, time)
