from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class MonitoredObject(Base):
    __tablename__ = "monitored_objects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    object_type = Column(String, nullable=False, default="service")
    address = Column(String, nullable=False)
    check_interval = Column(Integer, nullable=False, default=60)
    warning_threshold = Column(Integer, nullable=False, default=1000)
    critical_threshold = Column(Integer, nullable=False, default=3000)
    status = Column(String, nullable=False, default="normal")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_check_at = Column(DateTime, nullable=True)

    check_results = relationship("CheckResult", back_populates="object", cascade="all, delete-orphan")
    incidents = relationship("Incident", back_populates="object", cascade="all, delete-orphan")


class CheckResult(Base):
    __tablename__ = "check_results"

    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, ForeignKey("monitored_objects.id"), nullable=False)
    checked_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_available = Column(Boolean, nullable=False)
    response_time = Column(Integer, nullable=True)
    cpu_load = Column(Float, nullable=True)
    ram_usage = Column(Float, nullable=True)
    disk_usage = Column(Float, nullable=True)

    object = relationship("MonitoredObject", back_populates="check_results")


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    object_id = Column(Integer, ForeignKey("monitored_objects.id"), nullable=False)
    incident_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="open")

    object = relationship("MonitoredObject", back_populates="incidents")
    notifications = relationship("Notification", back_populates="incident", cascade="all, delete-orphan")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    sent_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    channel = Column(String, nullable=False)
    message_text = Column(Text, nullable=False)
    delivery_status = Column(String, nullable=False, default="sent")

    incident = relationship("Incident", back_populates="notifications")
