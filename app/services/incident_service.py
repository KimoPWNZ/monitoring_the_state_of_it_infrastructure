from datetime import datetime
from sqlalchemy.orm import Session

from ..models import Incident


def create_or_update_incident(
    session: Session,
    object_id: int,
    status: str,
    incident_type: str,
    measured_value: str | None,
) -> Incident:
    incident = (
        session.query(Incident)
        .filter(
            Incident.object_id == object_id,
            Incident.incident_type == incident_type,
            Incident.status == "open",
        )
        .order_by(Incident.created_at.desc())
        .first()
    )

    if incident:
        incident.last_seen = datetime.utcnow()
        incident.severity = status
        incident.measured_value = measured_value
        session.commit()
        return incident

    incident = Incident(
        object_id=object_id,
        incident_type=incident_type,
        severity=status,
        measured_value=measured_value,
    )
    session.add(incident)
    session.commit()
    session.refresh(incident)
    return incident


def close_open_incidents(session: Session, object_id: int) -> None:
    incidents = (
        session.query(Incident)
        .filter(Incident.object_id == object_id, Incident.status == "open")
        .all()
    )
    for incident in incidents:
        incident.status = "closed"
        incident.closed_at = datetime.utcnow()
    session.commit()
