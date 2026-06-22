import smtplib
from email.message import EmailMessage

from app import crud
from app.config import settings
from app.models import Incident, MonitoredObject


def _build_message(incident: Incident, obj: MonitoredObject) -> str:
    return (
        f"Обнаружен инцидент для '{obj.name}' ({obj.address}): "
        f"тип={incident.incident_type}, severity={incident.severity}."
    )


def create_internal_notification(db, incident: Incident, obj: MonitoredObject) -> None:
    crud.create_notification(
        db,
        incident_id=incident.id,
        channel="internal",
        message_text=_build_message(incident, obj),
        delivery_status="sent",
    )


def send_email_notification(incident: Incident, obj: MonitoredObject) -> str:
    if not settings.EMAIL_NOTIFICATIONS_ENABLED:
        return "failed"
    required = [settings.SMTP_SERVER, settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.SMTP_FROM]
    if not all(required):
        return "failed"

    message = EmailMessage()
    message["Subject"] = f"[CRITICAL] {obj.name}"
    message["From"] = settings.SMTP_FROM
    message["To"] = settings.SMTP_USERNAME
    message.set_content(_build_message(incident, obj))

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            smtp.send_message(message)
        return "sent"
    except Exception:  # noqa: BLE001
        return "failed"


def process_new_incident_notifications(db, incident: Incident, obj: MonitoredObject) -> None:
    create_internal_notification(db, incident, obj)

    if incident.severity == "critical":
        delivery_status = send_email_notification(incident, obj)
        crud.create_notification(
            db,
            incident_id=incident.id,
            channel="email",
            message_text=_build_message(incident, obj),
            delivery_status=delivery_status,
        )
