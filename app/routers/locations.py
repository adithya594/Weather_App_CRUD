from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from app.db import get_db
from app.services.location_service import list_locations, get_location, delete_location
from app.services.weather_service import resolve_location
from app.schemas.location import LocationRead

load_dotenv()

router = APIRouter()

@router.get("/from-coords")
def from_coords(lat: float, lon: float):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise HTTPException(500, "Missing OPENWEATHER_API_KEY in environment")
    _, _, place = resolve_location(f"{lat},{lon}", api_key)
    return RedirectResponse(url=f"/view?location={place}")

@router.get("/", response_model=List[LocationRead])
def read_locations(db: Session = Depends(get_db)):
    return list_locations(db)

@router.get("/{loc_id}", response_model=LocationRead)
def read_location(loc_id: int, db: Session = Depends(get_db)):
    loc = get_location(db, loc_id)
    if not loc:
        raise HTTPException(404, "Location not found")
    return loc

@router.delete("/{loc_id}")
def remove_location(loc_id: int, db: Session = Depends(get_db)):
    ok = delete_location(db, loc_id)
    if not ok:
        raise HTTPException(404, "Location not found")
    return {"detail": "deleted"}


