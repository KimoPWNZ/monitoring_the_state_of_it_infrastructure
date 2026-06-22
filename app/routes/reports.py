from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.report_service import build_report

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/api/reports")
def api_report(
    date_from: datetime,
    date_to: datetime,
    object_id: int | None = None,
    db: Session = Depends(get_db),
):
    if date_to < date_from:
        raise HTTPException(status_code=400, detail="date_to must be greater than or equal to date_from")
    return build_report(db, date_from, date_to, object_id=object_id)


@router.get("/reports", response_class=HTMLResponse)
def reports_page(
    request: Request,
    date_from: str | None = None,
    date_to: str | None = None,
    object_id: int | None = None,
    db: Session = Depends(get_db),
):
    report = None
    parsed_from = parsed_to = None
    if date_from and date_to:
        parsed_from = datetime.fromisoformat(date_from)
        parsed_to = datetime.fromisoformat(date_to)
        report = build_report(db, parsed_from, parsed_to, object_id=object_id)

    return templates.TemplateResponse(
        request=request,
        name="reports.html",
        context={
            "report": report,
            "objects": crud.get_objects(db),
            "selected_object_id": object_id,
            "date_from": parsed_from.date().isoformat() if parsed_from else "",
            "date_to": parsed_to.date().isoformat() if parsed_to else "",
        },
    )
