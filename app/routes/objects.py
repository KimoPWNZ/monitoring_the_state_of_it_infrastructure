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
