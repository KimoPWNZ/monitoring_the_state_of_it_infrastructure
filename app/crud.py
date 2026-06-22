from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas


def get_objects(db: Session, skip: int = 0, limit: int = 100) -> list[models.MonitoredObject]:
    return db.query(models.MonitoredObject).order_by(models.MonitoredObject.id).offset(skip).limit(limit).all()


def get_object(db: Session, object_id: int) -> models.MonitoredObject | None:
    return db.get(models.MonitoredObject, object_id)


def create_object(db: Session, payload: schemas.MonitoredObjectCreate) -> models.MonitoredObject:
    obj = models.MonitoredObject(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_object(db: Session, object_id: int, payload: schemas.MonitoredObjectUpdate) -> models.MonitoredObject | None:
    obj = get_object(db, object_id)
    if not obj:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_object(db: Session, object_id: int) -> bool:
    obj = get_object(db, object_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


def create_check_result(
    db: Session,
    object_id: int,
    available: bool,
    response_time: int | None,
    cpu_load: float | None = None,
    ram_usage: float | None = None,
    disk_usage: float | None = None,
) -> models.CheckResult:
    result = models.CheckResult(
        object_id=object_id,
        is_available=available,
        response_time=response_time,
        cpu_load=cpu_load,
        ram_usage=ram_usage,
        disk_usage=disk_usage,
    )
    db.add(result)
    db.flush()
    return result


def get_latest_check(db: Session, object_id: int) -> models.CheckResult | None:
    return (
        db.query(models.CheckResult)
        .filter(models.CheckResult.object_id == object_id)
        .order_by(models.CheckResult.checked_at.desc())
        .first()
    )


def get_recent_checks(db: Session, object_id: int, limit: int = 20) -> list[models.CheckResult]:
    return (
        db.query(models.CheckResult)
        .filter(models.CheckResult.object_id == object_id)
        .order_by(models.CheckResult.checked_at.desc())
        .limit(limit)
        .all()
    )


def get_incidents(
    db: Session,
    object_id: int | None = None,
    severity: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Incident]:
    query = db.query(models.Incident)
    if object_id is not None:
        query = query.filter(models.Incident.object_id == object_id)
    if severity is not None:
        query = query.filter(models.Incident.severity == severity)
    if date_from is not None:
        query = query.filter(models.Incident.created_at >= date_from)
    if date_to is not None:
        query = query.filter(models.Incident.created_at <= date_to)
    return query.order_by(models.Incident.created_at.desc()).offset(skip).limit(limit).all()


def get_open_incident_by_type(db: Session, object_id: int, incident_type: str) -> models.Incident | None:
    return (
        db.query(models.Incident)
        .filter(
            models.Incident.object_id == object_id,
            models.Incident.incident_type == incident_type,
            models.Incident.status == "open",
        )
        .first()
    )


def create_incident(db: Session, object_id: int, incident_type: str, severity: str) -> models.Incident:
    incident = models.Incident(object_id=object_id, incident_type=incident_type, severity=severity)
    db.add(incident)
    db.flush()
    return incident


def close_open_incidents(db: Session, object_id: int) -> list[models.Incident]:
    incidents = (
        db.query(models.Incident)
        .filter(models.Incident.object_id == object_id, models.Incident.status == "open")
        .all()
    )
    closed_at = datetime.utcnow()
    for incident in incidents:
        incident.status = "closed"
        incident.closed_at = closed_at
    return incidents


def create_notification(
    db: Session,
    incident_id: int,
    channel: str,
    message_text: str,
    delivery_status: str,
) -> models.Notification:
    notification = models.Notification(
        incident_id=incident_id,
        channel=channel,
        message_text=message_text,
        delivery_status=delivery_status,
    )
    db.add(notification)
    db.flush()
    return notification


def get_notifications(db: Session, object_id: int | None = None, limit: int = 100) -> list[models.Notification]:
    query = db.query(models.Notification).join(models.Incident, models.Notification.incident_id == models.Incident.id)
    if object_id is not None:
        query = query.filter(models.Incident.object_id == object_id)
    return query.order_by(models.Notification.sent_at.desc()).limit(limit).all()


def count_objects_by_status(db: Session) -> dict[str, int]:
    rows = db.query(models.MonitoredObject.status, func.count(models.MonitoredObject.id)).group_by(models.MonitoredObject.status).all()
    return {status: count for status, count in rows}
