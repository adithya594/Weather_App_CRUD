from sqlalchemy import Column, Integer, Float, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class Forecast(Base):
    __tablename__ = "forecasts"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    max_temp = Column(Float)
    min_temp = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    sunrise = Column(Time)
    sunset = Column(Time)

    location_id = Column(Integer, ForeignKey("locations.id"))
    location = relationship("Location", back_populates="forecasts")
