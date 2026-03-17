from datetime import datetime

from namozvaqti.cache import save_month
from namozvaqti.fetch import fetch_month
from namozvaqti.parse import parse_month
from namozvaqti.transform import enrich_with_timestamps

now = datetime.now()

html = fetch_month("namangan", now.month)
parsed = parse_month(html, now.year, now.month)
enriched = enrich_with_timestamps(parsed)

save_month(now.year, now.month, enriched)

print("Saved successfully.")
