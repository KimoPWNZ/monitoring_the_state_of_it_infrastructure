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
