from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..auth import require_user
from ..database import get_session
from ..models import MonitoredObject
from ..config import settings

router = APIRouter(prefix="/objects", tags=["objects"], dependencies=[Depends(require_user)])
templates = Jinja2Templates(directory="app/templates")


@router.get("")
def list_objects(request: Request, session: Session = Depends(get_session)):
    objects = session.query(MonitoredObject).order_by(MonitoredObject.id).all()
    return templates.TemplateResponse(
        "objects.html",
        {
            "request": request,
            "objects": objects,
            "settings": settings,
        },
    )


@router.post("")
def create_object(
    name: str = Form(...),
    object_type: str = Form("http"),
    address: str = Form(...),
    check_interval: int = Form(settings.default_check_interval),
    warning_threshold: float = Form(settings.warning_response_time),
    critical_threshold: float = Form(settings.critical_response_time),
    session: Session = Depends(get_session),
):
    obj = MonitoredObject(
        name=name,
        object_type=object_type,
        address=address,
        check_interval=check_interval,
        warning_threshold=warning_threshold,
        critical_threshold=critical_threshold,
    )
    session.add(obj)
    session.commit()
    return RedirectResponse(url="/objects", status_code=303)


@router.post("/{object_id}/delete")
def delete_object(object_id: int, session: Session = Depends(get_session)):
    obj = session.get(MonitoredObject, object_id)
    if obj:
        session.delete(obj)
        session.commit()
    return RedirectResponse(url="/objects", status_code=303)
