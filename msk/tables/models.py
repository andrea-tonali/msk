from sqlalchemy import Column, Integer, String, func, TIMESTAMP, ForeignKey

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class PatientJourneyScheduleWindow(Base):
    __tablename__ = "patient_journey_schedule_window"
    __table_args__ = {"comment": "PostgreSQL - MSK database"}
    patient_id = Column(Integer, primary_key=True)
    patient_journey_id = Column(Integer)
    activity_id = Column(Integer)
    activity_content_slug = Column(String)
    schedule_id = Column(Integer)
    schedule_slug = Column(String)
    schedule_start_offset_days = Column(Integer)  # Extracted field
    schedule_end_offset_days = Column(Integer)  # Extracted field
    schedule_milestone_slug = Column(String)  # Extracted field
    inserted_at = Column(
        TIMESTAMP, nullable=False, server_default=func.CURRENT_TIMESTAMP()
    )
