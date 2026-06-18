import psutil

from ...config import settings


def run_resource_check() -> dict:
    if not settings.local_agent_enabled:
        return {"available": False, "cpu_load": None, "ram_usage": None, "disk_usage": None}

    try:
        cpu_load = psutil.cpu_percent(interval=settings.local_agent_cpu_interval)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage(settings.local_agent_disk_path).percent
        return {
            "available": True,
            "cpu_load": round(cpu_load, 2),
            "ram_usage": round(ram_usage, 2),
            "disk_usage": round(disk_usage, 2),
        }
    except Exception:
        return {"available": False, "cpu_load": None, "ram_usage": None, "disk_usage": None}
