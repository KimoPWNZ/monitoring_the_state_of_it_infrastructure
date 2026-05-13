from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..auth import require_user
from ..database import get_session
from ..models import Incident, MonitoredObject
from ..schemas import MonitoredObjectCreate, MonitoredObjectRead, IncidentRead
from ..services.report_service import build_report, build_incident_metrics
from ..services.export_service import build_report_csv, build_report_pdf

router = APIRouter(prefix="/api", tags=["api"], dependencies=[Depends(require_user)])


@router.get("/objects", response_model=list[MonitoredObjectRead])
def api_list_objects(session: Session = Depends(get_session)):
    return session.query(MonitoredObject).order_by(MonitoredObject.id).all()


@router.post("/objects", response_model=MonitoredObjectRead)
def api_create_object(payload: MonitoredObjectCreate, session: Session = Depends(get_session)):
    obj = MonitoredObject(**payload.model_dump())
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.delete("/objects/{object_id}")
def api_delete_object(object_id: int, session: Session = Depends(get_session)):
    obj = session.get(MonitoredObject, object_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    session.delete(obj)
    session.commit()
    return {"status": "deleted"}


@router.get("/incidents", response_model=list[IncidentRead])
def api_list_incidents(session: Session = Depends(get_session)):
    return session.query(Incident).order_by(Incident.created_at.desc()).all()


@router.get("/reports")
def api_report(date_from: str, date_to: str, session: Session = Depends(get_session)):
    start = datetime.fromisoformat(date_from)
    end = datetime.fromisoformat(date_to)
    return build_report(session, start, end)


@router.get("/reports/export")
def api_report_export(
    format: str,
    date_from: str,
    date_to: str,
    session: Session = Depends(get_session),
):
    start = datetime.fromisoformat(date_from)
    end = datetime.fromisoformat(date_to)
    report = build_report(session, start, end)

    if format == "csv":
        data = build_report_csv(report)
        return {
            "filename": "report.csv",
            "content": data.decode("utf-8"),
        }

    if format == "pdf":
        data = build_report_pdf(report, date_from, date_to)
        return {
            "filename": "report.pdf",
            "content_base64": data.hex(),
        }

    raise HTTPException(status_code=400, detail="Unsupported format")


@router.get("/metrics/incidents")
def api_incident_metrics(date_from: str, date_to: str, session: Session = Depends(get_session)):
    start = datetime.fromisoformat(date_from)
    end = datetime.fromisoformat(date_to)
    return build_incident_metrics(session, start, end)
