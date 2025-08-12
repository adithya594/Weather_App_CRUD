import re
import requests
from collections import defaultdict
from datetime import datetime
from typing import List

from app.core.config import settings
from app.schemas.forecast import ForecastCreate

ZIP_RE = re.compile(r"^\d{5}(-\d{4})?$")

def resolve_location(location: str, api_key: str):
    location = location.strip()

    # gps lat,lon
    if "," in location and not location.endswith(","):
        parts = location.split(",", 1)
        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return lat, lon, f"{lat},{lon}"
        except ValueError:
            pass

    # ZIP
    if ZIP_RE.match(location) or ("," in location and location.split(",", 1)[0].strip().isdigit()):
        zip_param = location if "," in location else f"{location},US"
        r = requests.get(
            "http://api.openweathermap.org/geo/1.0/zip",
            params={"zip": zip_param, "appid": api_key},
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json()
            lat, lon = data["lat"], data["lon"]
            place = f'{data.get("name","")}, {data.get("country","")}'.strip(", ")
            return lat, lon, place

    # city / direct
    r = requests.get(
        "http://api.openweathermap.org/geo/1.0/direct",
        params={"q": location, "limit": 1, "appid": api_key},
        timeout=10,
    )
    arr = r.json()
    if arr:
        entry = arr[0]
        lat, lon = entry["lat"], entry["lon"]
        name = entry.get("name") or location
        state = entry.get("state", "")
        country = entry.get("country", "")
        pieces = [p for p in [name, state, country] if p]
        return lat, lon, ", ".join(pieces)

    raise Exception("Location not found")


def fetch_weather_raw(lat: float, lon: float, api_key: str):
    cur = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"lat": lat, "lon": lon, "appid": api_key, "units": "metric"},
        timeout=10,
    ).json()

    fc = requests.get(
        "https://api.openweathermap.org/data/2.5/forecast",
        params={"lat": lat, "lon": lon, "appid": api_key, "units": "metric"},
        timeout=10,
    ).json()

    return cur, fc


def summarize_forecast(fc_json) -> List[ForecastCreate]:
    buckets = defaultdict(list)
    for item in fc_json.get("list", []):
        day = datetime.utcfromtimestamp(item["dt"]).strftime("%Y-%m-%d")
        buckets[day].append(item)

    results: List[ForecastCreate] = []
    for day, items in list(buckets.items())[:5]:
        temps = [x["main"]["temp"] for x in items if "main" in x]
        feels = [x["main"].get("feels_like") for x in items if "main" in x]
        humid = [x["main"].get("humidity") for x in items if "main" in x]

        max_temp = round(max(temps), 1) if temps else None
        min_temp = round(min(temps), 1) if temps else None
        feels_like = round(sum([v for v in feels if v is not None]) / len([v for v in feels if v is not None]), 1) if feels else None
        humidity = int(round(sum([h for h in humid if h is not None]) / len([h for h in humid if h is not None]))) if humid else None

        srise = None
        sset = None

        results.append(
            ForecastCreate(
                date=datetime.strptime(day, "%Y-%m-%d").date(),
                max_temp=max_temp,
                min_temp=min_temp,
                feels_like=feels_like,
                humidity=humidity,
                sunrise=srise,
                sunset=sset,
            )
        )

    return results


def get_weather_and_forecasts(location: str):
    api_key = settings.OPENWEATHER_API_KEY
    if not api_key:
        raise Exception("Missing OPENWEATHER_API_KEY")

    lat, lon, place = resolve_location(location, api_key)
    current, forecast = fetch_weather_raw(lat, lon, api_key)
    forecasts = summarize_forecast(forecast)

    try:
        sunrise_ts = current.get("sys", {}).get("sunrise")
        sunset_ts = current.get("sys", {}).get("sunset")
        if forecasts:
            forecasts[0].sunrise = (datetime.utcfromtimestamp(sunrise_ts).time() if sunrise_ts else None)
            forecasts[0].sunset = (datetime.utcfromtimestamp(sunset_ts).time() if sunset_ts else None)
    except Exception:
        pass

    return place, lat, lon, current, forecasts
