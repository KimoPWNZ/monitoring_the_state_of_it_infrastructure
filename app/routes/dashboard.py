from datetime import datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.models import Incident, MonitoredObject

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _dashboard_payload(db: Session) -> schemas.DashboardResponse:
    objects = crud.get_objects(db)
    statuses = crud.count_objects_by_status(db)
    active_incidents = (
        db.query(Incident)
        .filter(Incident.status == "open")
        .order_by(Incident.created_at.desc())
        .limit(10)
        .all()
    )
    return schemas.DashboardResponse(objects=objects, status_counters=statuses, active_incidents=active_incidents)


@router.get("/api/dashboard", response_model=schemas.DashboardResponse)
def api_dashboard(db: Session = Depends(get_db)):
    return _dashboard_payload(db)


@router.get("/api/dashboard/table", response_class=HTMLResponse)
def api_dashboard_table(request: Request, db: Session = Depends(get_db)):
    objects = db.query(MonitoredObject).order_by(MonitoredObject.id).all()
    return templates.TemplateResponse(
        request=request,
        name="partials/dashboard_table.html",
        context={"objects": objects, "now": datetime.utcnow()},
    )


@router.get("/", response_class=HTMLResponse)
def dashboard_page(request: Request, db: Session = Depends(get_db)):
    payload = _dashboard_payload(db)
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"dashboard": payload},
    )
