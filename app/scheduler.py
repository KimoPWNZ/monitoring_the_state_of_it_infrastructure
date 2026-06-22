import asyncio
from datetime import datetime, timedelta

from app import crud
from app.check_service import run_check
from app.config import settings
from app.database import SessionLocal
from app.incident_service import process_status_change
from app.status_service import determine_status


async def _check_object(db, obj):
    result = await run_check(obj)
    new_status = determine_status(result, obj.warning_threshold, obj.critical_threshold)

    crud.create_check_result(
        db,
        object_id=obj.id,
        available=result["available"],
        response_time=result.get("response_time"),
        cpu_load=result.get("cpu_load"),
        ram_usage=result.get("ram_usage"),
        disk_usage=result.get("disk_usage"),
    )

    obj.status = new_status
    obj.last_check_at = datetime.utcnow()
    process_status_change(db, obj, new_status, result)


async def monitoring_loop() -> None:
    while True:
        db = SessionLocal()
        try:
            objects = crud.get_objects(db, skip=0, limit=10000)
            now = datetime.utcnow()
            for obj in objects:
                if obj.last_check_at is None or now - obj.last_check_at >= timedelta(seconds=obj.check_interval):
                    await _check_object(db, obj)
            db.commit()
        except Exception:  # noqa: BLE001
            db.rollback()
        finally:
            db.close()

        await asyncio.sleep(settings.MONITORING_LOOP_INTERVAL)
