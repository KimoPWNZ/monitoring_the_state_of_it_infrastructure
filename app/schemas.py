from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


StatusValue = Literal["normal", "warning", "critical"]


class MonitoredObjectBase(BaseModel):
    name: str = Field(min_length=1)
    object_type: str = "service"
    address: str = Field(min_length=1)
    check_interval: int = Field(default=60, ge=5)
    warning_threshold: int = Field(default=1000, ge=1)
    critical_threshold: int = Field(default=3000, ge=1)


class MonitoredObjectCreate(MonitoredObjectBase):
    pass


class MonitoredObjectUpdate(BaseModel):
    name: str | None = None
    object_type: str | None = None
    address: str | None = None
    check_interval: int | None = Field(default=None, ge=5)
    warning_threshold: int | None = Field(default=None, ge=1)
    critical_threshold: int | None = Field(default=None, ge=1)
    status: StatusValue | None = None


class CheckResultRead(BaseModel):
    id: int
    checked_at: datetime
    is_available: bool
    response_time: int | None
    cpu_load: float | None
    ram_usage: float | None
    disk_usage: float | None

    model_config = {"from_attributes": True}


class MonitoredObjectRead(MonitoredObjectBase):
    id: int
    status: StatusValue
    created_at: datetime
    last_check_at: datetime | None

    model_config = {"from_attributes": True}


class MonitoredObjectDetails(MonitoredObjectRead):
    latest_results: list[CheckResultRead]


class IncidentRead(BaseModel):
    id: int
    object_id: int
    incident_type: str
    severity: Literal["warning", "critical"]
    created_at: datetime
    closed_at: datetime | None
    status: Literal["open", "closed"]

    model_config = {"from_attributes": True}


class NotificationRead(BaseModel):
    id: int
    incident_id: int
    sent_at: datetime
    channel: Literal["internal", "email"]
    message_text: str
    delivery_status: Literal["sent", "failed"]

    model_config = {"from_attributes": True}


class DashboardResponse(BaseModel):
    objects: list[MonitoredObjectRead]
    status_counters: dict[str, int]
    active_incidents: list[IncidentRead]


class ReportRequest(BaseModel):
    date_from: datetime
    date_to: datetime
    object_id: int | None = None
