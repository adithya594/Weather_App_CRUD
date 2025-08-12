from pydantic import BaseModel
from typing import List
from app.schemas.forecast import ForecastCreate, ForecastRead

class LocationBase(BaseModel):
    name: str

class LocationCreate(LocationBase):
    forecasts: List[ForecastCreate]

class LocationRead(LocationBase):
    id: int
    forecasts: List[ForecastRead]

    class Config:
        orm_mode = True
