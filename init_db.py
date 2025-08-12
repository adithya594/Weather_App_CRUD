from app.db import Base, engine
import app.models.location  # to register models
import app.models.forecast

Base.metadata.create_all(bind=engine)
print("Database initialized")
