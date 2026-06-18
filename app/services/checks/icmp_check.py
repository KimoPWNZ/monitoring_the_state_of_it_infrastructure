import time
from urllib.parse import urlparse

from icmplib import ping

from ...config import settings


def _extract_host(address: str) -> str:
    parsed = urlparse(address if "://" in address else f"//{address}")
    return parsed.hostname or address.split(":")[0]


def run_icmp_check(address: str) -> dict:
    host = _extract_host(address)
    if not host:
        return {"available": False, "response_time": None}

    start_time = time.time()
    try:
        result = ping(
            host,
            count=1,
            interval=0,
            timeout=settings.icmp_timeout,
            privileged=False,
        )
        if not result:
            return {"available": False, "response_time": None}
        elapsed = result.avg_rtt
        if elapsed is None:
            elapsed = round((time.time() - start_time) * 1000, 2)
        return {"available": result.is_alive, "response_time": round(elapsed, 2)}
    except Exception:
        return {"available": False, "response_time": None}
