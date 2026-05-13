from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..auth import require_user
from ..database import get_session
from ..models import Incident

router = APIRouter(prefix="/incidents", tags=["incidents"], dependencies=[Depends(require_user)])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
def list_incidents(request: Request, session: Session = Depends(get_session)):
    incidents = (
        session.query(Incident)
        .order_by(Incident.status.desc(), Incident.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(
        "incidents.html", {"request": request, "incidents": incidents}
    )
