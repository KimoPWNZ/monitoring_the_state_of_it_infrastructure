from app import crud
from app.models import MonitoredObject
from app.notification_service import process_new_incident_notifications


def _incident_type_from_result(result: dict) -> str:
    if not result.get("available", False):
        return "availability"
    if result.get("response_time") is not None:
        return "response_time"
    return "availability"


def process_status_change(db, obj: MonitoredObject, new_status: str, result: dict) -> None:
    if new_status == "normal":
        crud.close_open_incidents(db, obj.id)
        return

    incident_type = _incident_type_from_result(result)
    existing = crud.get_open_incident_by_type(db, obj.id, incident_type)
    if existing:
        existing.severity = new_status
        return

    incident = crud.create_incident(db, obj.id, incident_type, new_status)
    process_new_incident_notifications(db, incident, obj)
