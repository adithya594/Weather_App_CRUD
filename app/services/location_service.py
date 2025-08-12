from sqlalchemy.orm import Session
from app import models, schemas

def create_location_with_forecasts(db: Session, name: str, forecasts: list[schemas.forecast.ForecastCreate]):
    db_loc = models.location.Location(name=name)
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)

    created = []
    for f in forecasts:
        db_f = models.forecast.Forecast(
            date=f.date,
            max_temp=f.max_temp,
            min_temp=f.min_temp,
            feels_like=f.feels_like,
            humidity=f.humidity,
            sunrise=f.sunrise,
            sunset=f.sunset,
            location_id=db_loc.id,
        )
        db.add(db_f)
        created.append(db_f)

    db.commit()
    db.refresh(db_loc)
    return db_loc

def list_locations(db: Session):
    return db.query(models.location.Location).all()

def get_location(db: Session, loc_id: int):
    return db.query(models.location.Location).filter(models.location.Location.id == loc_id).first()

def delete_location(db: Session, loc_id: int):
    loc = get_location(db, loc_id)
    if not loc:
        return False
    db.delete(loc)
    db.commit()
    return True
