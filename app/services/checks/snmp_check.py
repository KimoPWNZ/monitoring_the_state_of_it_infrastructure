import asyncio
import time
from urllib.parse import urlparse

from pysnmp.hlapi.v3arch import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    get_cmd,
)

from ...config import settings


def _extract_host(address: str) -> str:
    parsed = urlparse(address if "://" in address else f"//{address}")
    return parsed.hostname or address.split(":")[0]


def _to_float(value) -> float | None:
    try:
        return float(value.prettyPrint())
    except (ValueError, TypeError, AttributeError):
        return None


async def _snmp_get_async(host: str, oid: str):
    mp_model = 1 if settings.snmp_version == "2c" else 0
    transport = await UdpTransportTarget.create(
        (host, settings.snmp_port),
        timeout=settings.snmp_timeout,
        retries=settings.snmp_retries,
    )
    error_indication, error_status, _, var_binds = await get_cmd(
        SnmpEngine(),
        CommunityData(settings.snmp_community, mpModel=mp_model),
        transport,
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
    )
    if error_indication or error_status:
        raise RuntimeError("SNMP request failed")
    return var_binds[0][1]


def _snmp_get(host: str, oid: str):
    return asyncio.run(_snmp_get_async(host, oid))


def run_snmp_check(address: str) -> dict:
    host = _extract_host(address)
    if not host:
        return {"available": False, "response_time": None}

    start_time = time.time()
    try:
        _snmp_get(host, settings.snmp_uptime_oid)
        elapsed = round((time.time() - start_time) * 1000, 2)

        result = {"available": True, "response_time": elapsed}
        metric_oids = {
            "cpu_load": settings.snmp_cpu_oid,
            "ram_usage": settings.snmp_ram_oid,
            "disk_usage": settings.snmp_disk_oid,
        }
        for key, oid in metric_oids.items():
            if not oid:
                continue
            try:
                result[key] = _to_float(_snmp_get(host, oid))
            except Exception:
                result[key] = None
        return result
    except Exception:
        return {"available": False, "response_time": None}
