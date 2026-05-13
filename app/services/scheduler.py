from apscheduler.schedulers.background import BackgroundScheduler

from ..database import SessionLocal
from ..services.monitoring import monitoring_cycle

scheduler = BackgroundScheduler()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(run_cycle, "interval", seconds=10, id="monitoring_cycle")
        scheduler.start()


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)


def run_cycle():
    session = SessionLocal()
    try:
        monitoring_cycle(session)
    finally:
        session.close()
