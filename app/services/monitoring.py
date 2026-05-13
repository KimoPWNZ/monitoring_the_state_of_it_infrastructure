from datetime import datetime
from sqlalchemy.orm import Session

from ..models import MonitoredObject, CheckResult
from ..services.check_service import run_check
from ..services.status_service import define_status
from ..services.incident_service import create_or_update_incident, close_open_incidents
from ..services.notification_service import build_notification_text, save_notification, send_email


def process_object(session: Session, obj: MonitoredObject) -> None:
    result = run_check(obj.address, obj.object_type)
    status = define_status(result, obj.warning_threshold, obj.critical_threshold)

    obj.status = status
    obj.last_checked = datetime.utcnow()

    check_result = CheckResult(
        object_id=obj.id,
        is_available=result["available"],
        response_time=result.get("response_time"),
    )
    session.add(check_result)
    session.commit()

    if status in {"warning", "critical"}:
        incident_type = "availability" if not result["available"] else "response_time"
        measured_value = str(result.get("response_time")) if result.get("response_time") else None
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
