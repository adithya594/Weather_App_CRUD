from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.services.weather_service import get_weather_and_forecasts
from app.services.location_service import create_location_with_forecasts
from app.db import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    # keep original index template
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/view", response_class=HTMLResponse)
def view(request: Request, location: str, db: Session = Depends(get_db)):
    try:
        place, lat, lon, current, forecasts = get_weather_and_forecasts(location)
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "message": str(e)})

    # Save to DB: name + 5-day forecasts
    loc = create_location_with_forecasts(db, place, forecasts)

    now_icon = current.get("weather", [{}])[0].get("icon", "01d")

    return templates.TemplateResponse(            "view.html",            {                "request": request,                "place": place,                "lat": lat,                "lon": lon,                "current": current,                "now_icon_url": f"https://openweathermap.org/img/wn/{now_icon}@2x.png",                "days": [                    {                        "date": f.date.isoformat(),                        "min": f.min_temp,                        "max": f.max_temp,                        "main": f.main,                        "icon": f.icon,                    }                    for f in forecasts                ],            },        )
