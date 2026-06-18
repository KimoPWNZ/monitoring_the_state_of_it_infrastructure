from app.services import check_service


def test_run_check_unknown_type():
    result = check_service.run_check("example.com", "unknown")
    assert result == {
        "available": False,
        "response_time": None,
        "cpu_load": None,
        "ram_usage": None,
        "disk_usage": None,
    }


def test_run_check_http_extended_combines_http_and_resources(monkeypatch):
    monkeypatch.setattr(
        check_service,
        "run_http_check",
        lambda address: {"available": True, "response_time": 120.0},
    )
    monkeypatch.setattr(
        check_service,
        "run_resource_check",
        lambda: {"available": True, "cpu_load": 20.0, "ram_usage": 30.0, "disk_usage": 40.0},
    )

    result = check_service.run_check("https://example.com", "http_extended")

    assert result == {
        "available": True,
        "response_time": 120.0,
        "cpu_load": 20.0,
        "ram_usage": 30.0,
        "disk_usage": 40.0,
    }
