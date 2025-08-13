# Weather App — Enterprise refactor

1. copy files into folder
2. create a .env file (see .env.example)
3. python -m venv .venv
4. source .venv/bin/activate (or .\.venv\Scripts\activate on Windows)
5. pip install -r requirements.txt
6. uvicorn app.main:app --reload

The /view route now saves Location + 5-day forecasts into SQLite.
