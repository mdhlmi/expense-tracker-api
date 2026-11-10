# Expense Tracker API

A REST API for tracking expenses, built with Python, FastAPI and SQLite.

## Features
- Create, read, update, delete expenses
- Monthly and per-category spending reports
- Input validation and automated tests (pytest)

## Run locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs

## Run tests
```bash
pytest -v
```

## Endpoints
| Method | Path | Description |
|---|---|---|
| POST | /expenses | Add an expense |
| GET | /expenses | List all expenses |
| GET | /expenses/{id} | Get one expense |
| PUT | /expenses/{id} | Update an expense |
| DELETE | /expenses/{id} | Delete an expense |
| GET | /reports/monthly | Total per month |
| GET | /reports/category | Total per category |