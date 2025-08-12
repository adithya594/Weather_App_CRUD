from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    DATABASE_URL: str = "sqlite:///./weather.db"

    class Config:
        env_file = ".env"

settings = Settings()
