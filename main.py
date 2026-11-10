from datetime import date as date_type
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import database as db

app = FastAPI(title="Expense Tracker API")
db.init_db()


class ExpenseIn(BaseModel):
    amount: float = Field(gt=0, description="Must be greater than 0")
    category: str = Field(min_length=1)
    date: date_type
    note: Optional[str] = None


@app.post("/expenses", status_code=201)
def create_expense(expense: ExpenseIn):
    new_id = db.add_expense(
        expense.amount, expense.category, expense.date.isoformat(), expense.note
    )
    return db.get_expense(new_id)


@app.get("/expenses")
def list_expenses(category: Optional[str] = None, month: Optional[str] = None):
    return db.get_expenses_filtered(category, month)


@app.get("/expenses/{expense_id}")
def read_expense(expense_id: int):
    expense = db.get_expense(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.put("/expenses/{expense_id}")
def edit_expense(expense_id: int, expense: ExpenseIn):
    changed = db.update_expense(
        expense_id, expense.amount, expense.category, expense.date.isoformat(), expense.note
    )
    if changed == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db.get_expense(expense_id)


@app.delete("/expenses/{expense_id}")
def remove_expense(expense_id: int):
    if db.delete_expense(expense_id) == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"deleted": expense_id}


@app.get("/reports/monthly")
def report_monthly():
    return db.monthly_report()


@app.get("/reports/category")
def report_category():
    return db.category_report()