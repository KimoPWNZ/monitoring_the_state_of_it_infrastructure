from datetime import datetime

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/api/incidents", response_model=list[schemas.IncidentRead])
def api_list_incidents(
    object_id: int | None = None,
    severity: str | None = Query(default=None, pattern="^(warning|critical)$"),
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.get_incidents(db, object_id, severity, date_from, date_to, skip, limit)


@router.get("/incidents", response_class=HTMLResponse)
def incidents_page(
    request: Request,
    object_id: int | None = None,
    severity: str | None = None,
    db: Session = Depends(get_db),
):
    incidents = crud.get_incidents(db, object_id=object_id, severity=severity)
    objects = crud.get_objects(db)
    return templates.TemplateResponse(
        request=request,
        name="incidents.html",
        context={"incidents": incidents, "objects": objects, "selected_object_id": object_id, "selected_severity": severity},
    )
