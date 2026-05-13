from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import CheckResult, Incident, MonitoredObject


def build_report(session: Session, date_from: datetime, date_to: datetime) -> dict:
    total_checks = (
        session.query(CheckResult)
        .filter(CheckResult.checked_at >= date_from, CheckResult.checked_at <= date_to)
        .count()
    )
    total_incidents = (
        session.query(Incident)
        .filter(Incident.created_at >= date_from, Incident.created_at <= date_to)
        .count()
    )
    critical_incidents = (
        session.query(Incident)
        .filter(
            Incident.created_at >= date_from,
            Incident.created_at <= date_to,
            Incident.severity == "critical",
        )
        .count()
    )
    warning_incidents = (
        session.query(Incident)
        .filter(
            Incident.created_at >= date_from,
            Incident.created_at <= date_to,
            Incident.severity == "warning",
        )
        .count()
    )
    top_objects = (
        session.query(MonitoredObject.name, func.count(Incident.id).label("total"))
        .join(Incident, Incident.object_id == MonitoredObject.id)
        .filter(Incident.created_at >= date_from, Incident.created_at <= date_to)
        .group_by(MonitoredObject.name)
        .order_by(func.count(Incident.id).desc())
        .limit(5)
        .all()
    )

    return {
        "total_checks": total_checks,
        "total_incidents": total_incidents,
        "critical_incidents": critical_incidents,
        "warning_incidents": warning_incidents,
        "top_problem_objects": [item[0] for item in top_objects],
    }
