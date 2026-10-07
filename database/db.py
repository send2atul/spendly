import sqlite3
from datetime import date
from pathlib import Path

from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).resolve().parent.parent / "expense_tracker.db"

CATEGORIES = ("Food", "Transport", "Bills", "Health",
              "Entertainment", "Shopping", "Other")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at    TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS expenses (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    amount      REAL NOT NULL,
    category    TEXT NOT NULL,
    date        TEXT NOT NULL,
    description TEXT,
    created_at  TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

# (day of current month, amount, category, description)
SAMPLE_EXPENSES = (
    (1, 45.50, "Food", "Groceries"),
    (3, 12.00, "Transport", "Bus pass top-up"),
    (5, 120.00, "Bills", "Electricity bill"),
    (8, 30.00, "Health", "Pharmacy"),
    (12, 15.99, "Entertainment", "Streaming subscription"),
    (15, 60.25, "Shopping", "New shoes"),
    (20, 8.75, "Other", "Gift wrap"),
    (25, 22.40, "Food", "Dinner out"),
)


def get_db():
    """Return a SQLite connection with Row access and foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they don't exist. Safe to call repeatedly."""
    conn = get_db()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def _month_date(day):
    """Return a YYYY-MM-DD date in the current month, never in the future."""
    today = date.today()
    return today.replace(day=min(day, today.day)).isoformat()


def seed_db():
    """Insert a demo user and sample expenses, only if no users exist yet."""
    conn = get_db()
    try:
        if conn.execute("SELECT 1 FROM users LIMIT 1").fetchone():
            return

        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
        )
        user_id = cur.lastrowid

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) "
            "VALUES (?, ?, ?, ?, ?)",
            [
                (user_id, amount, category, _month_date(day), description)
                for day, amount, category, description in SAMPLE_EXPENSES
            ],
        )
        conn.commit()
    finally:
        conn.close()
