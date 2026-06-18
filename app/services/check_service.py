from .checks.http_check import run_http_check
from .checks.icmp_check import run_icmp_check
from .checks.resource_check import run_resource_check
from .checks.snmp_check import run_snmp_check
from .checks.tcp_check import run_tcp_check


def run_check(address: str, object_type: str = "http") -> dict:
    empty_result = {
        "available": False,
        "response_time": None,
        "cpu_load": None,
        "ram_usage": None,
        "disk_usage": None,
    }

    if object_type == "http":
        return {**empty_result, **run_http_check(address)}
    if object_type == "icmp":
        return {**empty_result, **run_icmp_check(address)}
    if object_type == "tcp":
        return {**empty_result, **run_tcp_check(address)}
    if object_type == "snmp":
        return {**empty_result, **run_snmp_check(address)}
    if object_type == "local":
        return {**empty_result, **run_resource_check()}
    if object_type == "http_extended":
        http_result = run_http_check(address)
        resource_result = run_resource_check()
        return {
            **empty_result,
            **http_result,
            **resource_result,
            "available": bool(http_result.get("available")) and bool(resource_result.get("available")),
        }

    return empty_result
