import time

import requests

from ...config import settings


def run_http_check(address: str) -> dict:
    start_time = time.time()
    try:
        response = requests.get(address, timeout=settings.request_timeout)
        elapsed = round((time.time() - start_time) * 1000, 2)
        return {"available": response.status_code < 500, "response_time": elapsed}
    except requests.RequestException:
        return {"available": False, "response_time": None}
