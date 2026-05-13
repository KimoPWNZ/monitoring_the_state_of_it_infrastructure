from datetime import datetime
import time
import requests

from ..config import settings


def run_check(address: str, object_type: str = "http") -> dict:
    if object_type != "http":
        return {"available": False, "response_time": None}

    start_time = time.time()
    try:
        response = requests.get(address, timeout=settings.request_timeout)
        elapsed = round((time.time() - start_time) * 1000, 2)
        return {"available": response.status_code < 500, "response_time": elapsed}
    except requests.RequestException:
        return {"available": False, "response_time": None}
