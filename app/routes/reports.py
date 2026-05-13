from datetime import datetime
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_session
from ..services.report_service import build_report

router = APIRouter(prefix="/reports", tags=["reports"])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
def reports(request: Request, date_from: str | None = None, date_to: str | None = None, session: Session = Depends(get_session)):
    if not date_from or not date_to:
        return templates.TemplateResponse(
            "reports.html",
            {"request": request, "report": None, "date_from": None, "date_to": None},
        )

    start = datetime.fromisoformat(date_from)
    end = datetime.fromisoformat(date_to)
    report = build_report(session, start, end)
    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request,
            "report": report,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
