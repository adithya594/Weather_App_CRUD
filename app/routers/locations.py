from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.services.location_service import list_locations, get_location, delete_location
from app.schemas.location import LocationRead

router = APIRouter()

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
