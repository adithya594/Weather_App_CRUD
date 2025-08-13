from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import weather, locations
from app.core.config import settings

app = FastAPI(title="Weather App", version="1.0.0")

# templates & static (keeps your existing front-end intact)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# include routers
app.include_router(weather.router, prefix="", tags=["Weather"])
# Corrected line: removed the prefix so the URL path matches the front-end code
app.include_router(locations.router, prefix="", tags=["Locations"]) 

@app.get("/health")
def health():
    return {"status": "ok"}