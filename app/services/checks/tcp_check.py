import socket
import time
from urllib.parse import urlparse

from ...config import settings


def _parse_host_port(address: str) -> tuple[str | None, int]:
    if "://" in address:
        parsed = urlparse(address)
        host = parsed.hostname
        if parsed.port:
            return host, parsed.port
        if parsed.scheme == "https":
            return host, 443
        if parsed.scheme == "http":
            return host, 80
        return host, settings.default_tcp_port

    host, sep, port = address.rpartition(":")
    if sep and host:
        try:
            return host, int(port)
        except ValueError:
            return None, settings.default_tcp_port
    return address, settings.default_tcp_port


def run_tcp_check(address: str) -> dict:
    host, port = _parse_host_port(address)
    if not host:
        return {"available": False, "response_time": None}

    start_time = time.time()
    try:
        with socket.create_connection((host, port), timeout=settings.request_timeout):
            elapsed = round((time.time() - start_time) * 1000, 2)
            return {"available": True, "response_time": elapsed}
    except OSError:
        return {"available": False, "response_time": None}
