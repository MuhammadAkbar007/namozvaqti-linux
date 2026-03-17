# src/namoz/parse.py

from bs4 import BeautifulSoup


def parse_month(html: str, year: int, month: int) -> dict:
    soup = BeautifulSoup(html, "lxml")

    table = soup.select_one("table.table_calendar")
    if not table:
        raise RuntimeError("Prayer table not found")

    rows = table.select("tr")

    if len(rows) < 2:
        raise RuntimeError("Table has no data rows")

    data = {}

    for row in rows[1:]:  # skip header
        cols = [td.get_text(strip=True) for td in row.find_all("td")]

        # defensive check
        if len(cols) < 7:
            continue

        # "17 Tue" → 17
        day_str = cols[0].split()[0]
        day = int(day_str)

        date_key = f"{year:04d}-{month:02d}-{day:02d}"

        data[date_key] = {
            "Fajr": cols[1],
            "Sunrise": cols[2],  # shuruk
            "Dhuhr": cols[3],
            "Asr": cols[4],
            "Maghrib": cols[5],
            "Isha": cols[6],
        }

    if not data:
        raise RuntimeError("Parsed data is empty")

    return data
