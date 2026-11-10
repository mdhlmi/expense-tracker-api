import os

os.environ["EXPENSE_DB"] = "test_expenses.db"  # must be set before importing the app

import pytest
from fastapi.testclient import TestClient

import database as db
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    conn = db.get_connection()
    conn.execute("DELETE FROM expenses")
    conn.commit()
    conn.close()
    yield


def make(amount=10, category="food", date="2026-11-10", note="x"):
    return client.post(
        "/expenses",
        json={"amount": amount, "category": category, "date": date, "note": note},
    )


def test_create_and_list():
    r = make()
    assert r.status_code == 201
    assert r.json()["category"] == "food"
    assert len(client.get("/expenses").json()) == 1


def test_rejects_negative_amount():
    assert make(amount=-5).status_code == 422


def test_rejects_bad_date():
    assert make(date="not-a-date").status_code == 422


def test_update():
    expense_id = make().json()["id"]
    r = client.put(
        f"/expenses/{expense_id}",
        json={"amount": 99, "category": "travel", "date": "2026-11-11"},
    )
    assert r.status_code == 200
    assert r.json()["amount"] == 99


def test_delete_and_404():
    expense_id = make().json()["id"]
    assert client.delete(f"/expenses/{expense_id}").status_code == 200
    assert client.get(f"/expenses/{expense_id}").status_code == 404


def test_monthly_report():
    make(amount=10, date="2026-10-05")
    make(amount=20, date="2026-10-20")
    make(amount=5, date="2026-11-01")
    result = client.get("/reports/monthly").json()
    assert result == [
        {"month": "2026-10", "total": 30.0},
        {"month": "2026-11", "total": 5.0},
    ]


def test_category_report():
    make(amount=10, category="food")
    make(amount=15, category="food")
    make(amount=40, category="travel")
    result = client.get("/reports/category").json()
    assert result[0] == {"category": "travel", "total": 40.0}
    assert result[1] == {"category": "food", "total": 25.0}