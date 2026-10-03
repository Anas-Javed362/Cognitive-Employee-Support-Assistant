$env:PYTHONPATH=".\backend"
.\.venv\Scripts\python.exe scripts/seed_database.py
.\.venv\Scripts\python.exe scripts/ingest_knowledge.py

Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WorkingDirectory "frontend"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload --port 8000
