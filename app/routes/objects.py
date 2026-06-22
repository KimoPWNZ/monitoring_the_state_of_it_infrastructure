from fastapi import APIRouter, Depends, Form, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import crud, schemas
from app.config import settings
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/api/objects", response_model=list[schemas.MonitoredObjectRead])
def api_list_objects(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return crud.get_objects(db, skip=skip, limit=limit)


@router.post("/api/objects", response_model=schemas.MonitoredObjectRead)
def api_create_object(payload: schemas.MonitoredObjectCreate, db: Session = Depends(get_db)):
    return crud.create_object(db, payload)


@router.get("/api/objects/{object_id}", response_model=schemas.MonitoredObjectDetails)
def api_get_object(object_id: int, db: Session = Depends(get_db)):
    obj = crud.get_object(db, object_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return schemas.MonitoredObjectDetails(
        **schemas.MonitoredObjectRead.model_validate(obj).model_dump(),
        latest_results=[schemas.CheckResultRead.model_validate(item) for item in crud.get_recent_checks(db, object_id)],
    )


@router.put("/api/objects/{object_id}", response_model=schemas.MonitoredObjectRead)
def api_update_object(object_id: int, payload: schemas.MonitoredObjectUpdate, db: Session = Depends(get_db)):
    obj = crud.update_object(db, object_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return obj


@router.delete("/api/objects/{object_id}")
def api_delete_object(object_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_object(db, object_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Object not found")
    return {"status": "deleted"}


@router.get("/objects", response_class=HTMLResponse)
def objects_page(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request,
        name="objects.html",
        context={"objects": crud.get_objects(db), "settings": settings},
    )


@router.get("/objects/table", response_class=HTMLResponse)
def objects_table_partial(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        request=request,
        name="partials/objects_table.html",
        context={"objects": crud.get_objects(db)},
    )


@router.post("/objects/create", response_class=HTMLResponse)
def objects_create_from_form(
    request: Request,
    name: str = Form(...),
    object_type: str = Form("service"),
    address: str = Form(...),
    check_interval: int = Form(default=settings.DEFAULT_CHECK_INTERVAL),
    warning_threshold: int = Form(default=settings.WARNING_RESPONSE_TIME),
    critical_threshold: int = Form(default=settings.CRITICAL_RESPONSE_TIME),
    db: Session = Depends(get_db),
):
    payload = schemas.MonitoredObjectCreate(
        name=name,
        object_type=object_type,
        address=address,
        check_interval=check_interval,
        warning_threshold=warning_threshold,
        critical_threshold=critical_threshold,
    )
    crud.create_object(db, payload)
    return templates.TemplateResponse(
        request=request,
        name="partials/objects_table.html",
        context={"objects": crud.get_objects(db)},
    )


@router.post("/objects/{object_id}/delete", response_class=HTMLResponse)
def objects_delete_from_form(object_id: int, request: Request, db: Session = Depends(get_db)):
    crud.delete_object(db, object_id)
    return templates.TemplateResponse(
        request=request,
        name="partials/objects_table.html",
        context={"objects": crud.get_objects(db)},
    )
