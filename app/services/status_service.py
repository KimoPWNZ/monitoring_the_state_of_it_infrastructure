def define_status(result: dict, warning_limit: float, critical_limit: float) -> str:
    if not result["available"]:
        return "critical"
    response_time = result.get("response_time")
    if response_time is None:
        return "critical"
    if response_time >= critical_limit:
        return "critical"
    if response_time >= warning_limit:
        return "warning"
    return "normal"
