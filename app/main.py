from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .auth import require_user
from .database import Base, engine
from .routes import objects, incidents, reports, api
from .services.scheduler import start_scheduler, shutdown_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Monitoring System")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(objects.router)
app.include_router(incidents.router)
app.include_router(reports.router)
app.include_router(api.router)


@app.get("/")
def index(request: Request, user: str = Depends(require_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.on_event("startup")
def on_startup():
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()
