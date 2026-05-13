from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import MonitoredObject, Incident
from app.services.report_service import build_report


def test_build_report_counts():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    session = Session()
    obj = MonitoredObject(name="test", address="https://example.com")
    session.add(obj)
    session.commit()

    incident = Incident(object_id=obj.id, incident_type="availability", severity="critical")
    session.add(incident)
    session.commit()

    report = build_report(session, incident.created_at, incident.created_at)
    assert report["total_incidents"] == 1
