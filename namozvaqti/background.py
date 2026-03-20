import threading

_running = set()


def ensure_month_async(year: int, month: int):
    key = f"{year}-{month:02d}"

    if key in _running:
        return  # already fetching

    _running.add(key)

    thread = threading.Thread(
        target=_worker,
        args=(year, month, key),
        daemon=True,
    )
    thread.start()


def _worker(year: int, month: int, key: str):
    from namozvaqti.cache import save_month
    from namozvaqti.fetch import fetch_month
    from namozvaqti.parse import parse_month
    from namozvaqti.transform import enrich_with_timestamps

    try:
        html = fetch_month("namangan", month)
        parsed = parse_month(html, year, month)
        enriched = enrich_with_timestamps(parsed)

        save_month(year, month, enriched)

        print(f"[Background] Cached {key}")

    except Exception as e:
        print(f"[Background] Failed {key}: {e}")

    finally:
        _running.remove(key)
