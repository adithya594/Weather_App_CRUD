from pydantic import BaseModel
from datetime import date, time

class ForecastBase(BaseModel):
    date: date
    max_temp: float | None
    min_temp: float | None
    feels_like: float | None
    humidity: int | None
    sunrise: time | None
    sunset: time | None

class ForecastCreate(ForecastBase):
    pass

class ForecastRead(ForecastBase):
    id: int

    class Config:
        orm_mode = True
