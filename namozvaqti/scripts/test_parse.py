# scripts/test_parse.py

import json
from datetime import datetime

from namozvaqti.fetch import fetch_month
from namozvaqti.parse import parse_month

now = datetime.now()

html = fetch_month("namangan", now.month)
data = parse_month(html, now.year, now.month)

print(json.dumps(data, indent=2))
