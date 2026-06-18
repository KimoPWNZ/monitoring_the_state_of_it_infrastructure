from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import CheckResult, MonitoredObject
from app.services import monitoring


def test_process_object_saves_resource_metrics(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    obj = MonitoredObject(name="local", object_type="local", address="localhost")
    session.add(obj)
    session.commit()
    session.refresh(obj)

    monkeypatch.setattr(
        monitoring,
        "run_check",
        lambda address, object_type: {
            "available": True,
            "response_time": None,
            "cpu_load": 81.0,
            "ram_usage": 32.0,
            "disk_usage": 22.0,
        },
    )

    monitoring.process_object(session, obj)

    result = session.query(CheckResult).filter(CheckResult.object_id == obj.id).first()
    assert result is not None
    assert result.cpu_load == 81.0
    assert result.ram_usage == 32.0
    assert result.disk_usage == 22.0
