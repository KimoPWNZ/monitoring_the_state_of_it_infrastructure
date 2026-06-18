from ..config import settings


def define_status(result: dict, warning_limit: float, critical_limit: float) -> str:
    if not result["available"]:
        return "critical"

    has_warning = False

    response_time = result.get("response_time")
    if response_time is not None:
        if response_time >= critical_limit:
            return "critical"
        if response_time >= warning_limit:
            has_warning = True

    resource_limits = (
        ("cpu_load", settings.warning_cpu_load, settings.critical_cpu_load),
        ("ram_usage", settings.warning_ram_usage, settings.critical_ram_usage),
        ("disk_usage", settings.warning_disk_usage, settings.critical_disk_usage),
    )
    for key, warning_threshold, critical_threshold in resource_limits:
        value = result.get(key)
        if value is None:
            continue
        if value >= critical_threshold:
            return "critical"
        if value >= warning_threshold:
            has_warning = True

    if has_warning:
        return "warning"
    return "normal"
