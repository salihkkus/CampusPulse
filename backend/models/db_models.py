from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from database import Base

class EnergyRecordDB(Base):
    __tablename__ = "energy_records"

    id = Column(Integer, primary_key=True, index=True)
    record_date = Column(Date, index=True)
    room_id = Column(String, index=True)
    hour_of_day = Column(Integer)
    is_class_in_session = Column(Integer)
    lighting_watt = Column(Float)
    projector_watt = Column(Float)
    plug_load_watt = Column(Float)
    total_watt = Column(Float)
    is_anomaly = Column(Integer)
    wasted_cost_tl = Column(Float)
    is_holiday = Column(Integer)
    is_weekend = Column(Integer)
    uploaded_at = Column(DateTime)
