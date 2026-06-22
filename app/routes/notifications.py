from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/api/notifications", response_model=list[schemas.NotificationRead])
def api_list_notifications(object_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_notifications(db, object_id=object_id)


@router.get("/notifications", response_class=HTMLResponse)
def notifications_page(request: Request, object_id: int | None = None, db: Session = Depends(get_db)):
    notifications = crud.get_notifications(db, object_id=object_id)
    objects = crud.get_objects(db)
    return templates.TemplateResponse(
        request=request,
        name="notifications.html",
        context={"notifications": notifications, "objects": objects, "selected_object_id": object_id},
    )
