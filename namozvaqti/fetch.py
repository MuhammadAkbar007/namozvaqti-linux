import time

import requests


def fetch_month(region: str, month: int) -> str:
    if not 1 <= month <= 12:
        raise ValueError(f"Invalid month: {month}")

    url = f"https://namozvaqti.uz/en/oylik/{month}/{region}"
    headers = {"User-Agent": "namoz-cli/1.0 (+linux)"}

    attempts = 3
    delay = 2

    for i in range(attempts):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            return res.text

        except requests.RequestException as e:
            if i == attempts - 1:
                raise e  # final failure

            time.sleep(delay * (i + 1))  # linear backoff

    # satisfies type checker (even though unreachable)
    raise RuntimeError("Unreachable: fetch_month exhausted retries")
