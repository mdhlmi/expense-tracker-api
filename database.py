import os
import sqlite3

DB_NAME = os.getenv("EXPENSE_DB", "expenses.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL CHECK (amount > 0),
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                note TEXT
            )
        """)
        conn.commit()
    finally:
        conn.close()


def add_expense(amount, category, date, note):
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO expenses (amount, category, date, note) VALUES (?, ?, ?, ?)",
            (amount, category, date, note),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_expenses():
    conn = get_connection()
    try:
        rows = conn.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_expense(expense_id):
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_expense(expense_id, amount, category, date, note):
    conn = get_connection()
    try:
        cur = conn.execute(
            "UPDATE expenses SET amount = ?, category = ?, date = ?, note = ? WHERE id = ?",
            (amount, category, date, note, expense_id),
        )
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def delete_expense(expense_id):
    conn = get_connection()
    try:
        cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


def monthly_report():
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT substr(date, 1, 7) AS month, ROUND(SUM(amount), 2) AS total
            FROM expenses
            GROUP BY month
            ORDER BY month
        """).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def category_report():
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT category, ROUND(SUM(amount), 2) AS total
            FROM expenses
            GROUP BY category
            ORDER BY total DESC
        """).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_expenses_filtered(category=None, month=None):
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    if category:
        query += " AND category = ?"
        params.append(category)
    if month:
        query += " AND substr(date, 1, 7) = ?"
        params.append(month)
    query += " ORDER BY date DESC, id DESC"
    conn = get_connection()
    try:
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()