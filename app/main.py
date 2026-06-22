import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routes import dashboard, incidents, notifications, objects, reports
from app.scheduler import monitoring_loop

app = FastAPI(title="Monitoring System")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(dashboard.router)
app.include_router(objects.router)
app.include_router(incidents.router)
app.include_router(reports.router)
app.include_router(notifications.router)


@app.on_event("startup")
async def startup_event() -> None:
    app.state.monitoring_task = asyncio.create_task(monitoring_loop())


@app.on_event("shutdown")
async def shutdown_event() -> None:
    task = getattr(app.state, "monitoring_task", None)
    if task:
        task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task
