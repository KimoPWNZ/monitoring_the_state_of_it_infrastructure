from datetime import datetime

from sqlalchemy import func

from app.models import CheckResult, Incident, MonitoredObject


def build_report(db, date_from: datetime, date_to: datetime, object_id: int | None = None) -> dict:
    checks_query = db.query(CheckResult).filter(CheckResult.checked_at >= date_from, CheckResult.checked_at <= date_to)
    incidents_query = db.query(Incident).filter(Incident.created_at >= date_from, Incident.created_at <= date_to)
    if object_id is not None:
        checks_query = checks_query.filter(CheckResult.object_id == object_id)
        incidents_query = incidents_query.filter(Incident.object_id == object_id)

    incidents = incidents_query.all()

    by_type: dict[str, int] = {}
    by_severity: dict[str, int] = {"warning": 0, "critical": 0}
    for item in incidents:
        by_type[item.incident_type] = by_type.get(item.incident_type, 0) + 1
        by_severity[item.severity] = by_severity.get(item.severity, 0) + 1

    downtime_rows = (
        db.query(
            Incident.object_id,
            func.sum(
                func.coalesce(
                    func.julianday(Incident.closed_at) - func.julianday(Incident.created_at),
                    func.julianday(func.current_timestamp()) - func.julianday(Incident.created_at),
                )
            ),
        )
        .filter(
            Incident.severity == "critical",
            Incident.created_at >= date_from,
            Incident.created_at <= date_to,
        )
        .group_by(Incident.object_id)
        .all()
    )

    if object_id is not None:
        downtime_rows = [row for row in downtime_rows if row[0] == object_id]

    downtime_by_object: dict[str, float] = {}
    for object_ref, days in downtime_rows:
        obj = db.get(MonitoredObject, object_ref)
        if obj and days is not None:
            downtime_by_object[obj.name] = round(float(days) * 24 * 3600, 2)

    top_objects_query = (
        db.query(MonitoredObject.name, func.count(Incident.id).label("total_incidents"))
        .join(Incident, Incident.object_id == MonitoredObject.id)
        .filter(Incident.created_at >= date_from, Incident.created_at <= date_to)
        .group_by(MonitoredObject.name)
        .order_by(func.count(Incident.id).desc())
        .limit(5)
    )
    if object_id is not None:
        top_objects_query = top_objects_query.filter(MonitoredObject.id == object_id)

    top_objects = [
        {"name": name, "total_incidents": total_incidents}
        for name, total_incidents in top_objects_query.all()
    ]

    return {
        "date_from": date_from.isoformat(),
        "date_to": date_to.isoformat(),
        "total_checks": checks_query.count(),
        "total_incidents": len(incidents),
        "incidents_by_type": by_type,
        "incidents_by_severity": by_severity,
        "downtime_by_object_seconds": downtime_by_object,
        "top_problem_objects": top_objects,
    }
