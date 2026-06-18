from datetime import datetime
from sqlalchemy.orm import Session

from ..config import settings
from ..models import MonitoredObject, CheckResult
from ..services.check_service import run_check
from ..services.status_service import define_status
from ..services.incident_service import create_or_update_incident, close_open_incidents
from ..services.notification_service import build_notification_text, save_notification, send_email


def _resolve_incident(result: dict, warning_limit: float, critical_limit: float) -> tuple[str, str | None]:
    if not result["available"]:
        return "availability", None

    response_time = result.get("response_time")
    if response_time is not None and response_time >= warning_limit:
        return "response_time", str(response_time)

    resource_limits = (
        ("cpu_load", "cpu_load", settings.warning_cpu_load),
        ("ram_usage", "ram_usage", settings.warning_ram_usage),
        ("disk_usage", "disk_usage", settings.warning_disk_usage),
    )
    for key, incident_type, warning_threshold in resource_limits:
        value = result.get(key)
        if value is not None and value >= warning_threshold:
            return incident_type, str(value)

    return "availability", None


def process_object(session: Session, obj: MonitoredObject) -> None:
    result = run_check(obj.address, obj.object_type)
    status = define_status(result, obj.warning_threshold, obj.critical_threshold)

    obj.status = status
    obj.last_checked = datetime.utcnow()

    check_result = CheckResult(
        object_id=obj.id,
        is_available=result["available"],
        response_time=result.get("response_time"),
        cpu_load=result.get("cpu_load"),
        ram_usage=result.get("ram_usage"),
        disk_usage=result.get("disk_usage"),
    )
    session.add(check_result)
    session.commit()

    if status in {"warning", "critical"}:
        incident_type, measured_value = _resolve_incident(
            result,
            obj.warning_threshold,
            obj.critical_threshold,
        )
        incident = create_or_update_incident(
            session,
            object_id=obj.id,
            status=status,
            incident_type=incident_type,
            measured_value=measured_value,
        )

        message_text = build_notification_text(obj.name, status, measured_value)
        save_notification(session, incident.id, "ui", message_text, "sent")

        if status == "critical":
            email_status = send_email(message_text)
            save_notification(session, incident.id, "email", message_text, email_status)
    else:
        close_open_incidents(session, obj.id)


def monitoring_cycle(session: Session) -> None:
    objects = session.query(MonitoredObject).all()
    now = datetime.utcnow()
    for obj in objects:
        if obj.last_checked is None:
            process_object(session, obj)
            continue
        elapsed = (now - obj.last_checked).total_seconds()
        if elapsed >= obj.check_interval:
            process_object(session, obj)
