from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..auth import require_user
from ..database import get_session
from ..services.report_service import build_report
from ..services.export_service import build_report_csv, build_report_pdf

router = APIRouter(prefix="/reports", tags=["reports"], dependencies=[Depends(require_user)])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
def reports(
    request: Request,
    date_from: str | None = None,
    date_to: str | None = None,
    session: Session = Depends(get_session),
):
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


@router.get("/export")
def export_report(
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
        return Response(
            content=data,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=report.csv"},
        )

    if format == "pdf":
        data = build_report_pdf(report, date_from, date_to)
        return Response(
            content=data,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=report.pdf"},
        )

    raise HTTPException(status_code=400, detail="Unsupported format")
