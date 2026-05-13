import smtplib
from email.message import EmailMessage
from sqlalchemy.orm import Session

from ..config import settings
from ..models import Notification


def build_notification_text(object_name: str, status: str, measured_value: str | None) -> str:
    value_part = f", значение {measured_value}" if measured_value else ""
    return f"Объект {object_name}: статус {status}{value_part}"


def send_email(message_text: str) -> str:
    if not settings.email_notifications:
        return "disabled"
    if not all(
        [
            settings.smtp_server,
            settings.smtp_username,
            settings.smtp_password,
            settings.smtp_from,
            settings.smtp_to,
        ]
    ):
        return "not_configured"

    message = EmailMessage()
    message["Subject"] = "Monitoring alert"
    message["From"] = settings.smtp_from
    message["To"] = settings.smtp_to
    message.set_content(message_text)

    with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as smtp:
        smtp.starttls()
        smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)

    return "sent"


def save_notification(
    session: Session, incident_id: int, channel: str, message_text: str, delivery_status: str
) -> Notification:
    notification = Notification(
        incident_id=incident_id,
        channel=channel,
        message_text=message_text,
        delivery_status=delivery_status,
    )
    session.add(notification)
    session.commit()
    return notification
