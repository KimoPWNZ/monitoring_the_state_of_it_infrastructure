import time

import httpx

from app.config import settings
from app.models import MonitoredObject


async def run_check(obj: MonitoredObject) -> dict:
    try:
        async with httpx.AsyncClient(timeout=settings.REQUEST_TIMEOUT) as client:
            started = time.perf_counter()
            response = await client.get(obj.address)
            elapsed = (time.perf_counter() - started) * 1000
            return {
                "available": response.status_code < 400,
                "response_time": int(round(elapsed)),
                "error": None,
            }
    except Exception as exc:  # noqa: BLE001
        return {
            "available": False,
            "response_time": None,
            "error": str(exc),
        }
