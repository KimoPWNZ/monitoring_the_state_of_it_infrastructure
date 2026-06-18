from app.services.status_service import define_status


def test_define_status_normal():
    result = {"available": True, "response_time": 200}
    assert define_status(result, 1000, 3000) == "normal"


def test_define_status_warning():
    result = {"available": True, "response_time": 1500}
    assert define_status(result, 1000, 3000) == "warning"


def test_define_status_critical():
    result = {"available": False, "response_time": None}
    assert define_status(result, 1000, 3000) == "critical"


def test_define_status_normal_for_local_metrics():
    result = {"available": True, "response_time": None, "cpu_load": 30, "ram_usage": 40, "disk_usage": 50}
    assert define_status(result, 1000, 3000) == "normal"


def test_define_status_warning_for_cpu():
    result = {"available": True, "response_time": None, "cpu_load": 80, "ram_usage": 40, "disk_usage": 50}
    assert define_status(result, 1000, 3000) == "warning"


def test_define_status_critical_for_disk():
    result = {"available": True, "response_time": None, "cpu_load": 30, "ram_usage": 40, "disk_usage": 96}
    assert define_status(result, 1000, 3000) == "critical"
