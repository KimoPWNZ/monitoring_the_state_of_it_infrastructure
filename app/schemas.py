from pydantic import BaseModel


class MonitoredObjectCreate(BaseModel):
    name: str
    object_type: str = "http"
    address: str
    check_interval: int = 60
    warning_threshold: float = 1000
    critical_threshold: float = 3000


class MonitoredObjectRead(BaseModel):
    id: int
    name: str
    object_type: str
    address: str
    check_interval: int
    warning_threshold: float
    critical_threshold: float
    status: str

    model_config = {"from_attributes": True}


class IncidentRead(BaseModel):
    id: int
    object_id: int
    incident_type: str
    severity: str
    measured_value: str | None
    created_at: str
    status: str

    model_config = {"from_attributes": True}


class ReportSummary(BaseModel):
    total_checks: int
    total_incidents: int
    critical_incidents: int
    warning_incidents: int
    top_problem_objects: list[str]
