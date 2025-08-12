1. copy files into folder
2. create a .env file (see .env.example)
3. python -m venv .venv
4. .\.venv\Scripts\activate
5. pip install -r requirements.txt
6. uvicorn app.main:app --reload
7. Run the app in debug mode: uvicorn app.main:app --reload --log-level debug
8. Initialize db: python init_db.py
9. 

The /view route now saves Location + 5-day forecasts into MySQL.
