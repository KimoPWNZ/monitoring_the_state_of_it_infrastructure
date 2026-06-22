def determine_status(result: dict, warning_threshold: int, critical_threshold: int) -> str:
    if not result.get("available", False):
        return "critical"

    response_time = result.get("response_time")
    if response_time is None:
        return "normal"

    if response_time >= critical_threshold:
        return "critical"
    if response_time >= warning_threshold:
        return "warning"
    return "normal"
