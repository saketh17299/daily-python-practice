import sqlite3

DB_NAME = "weather_journal.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT NOT NULL,
            weather TEXT NOT NULL,
            mood TEXT NOT NULL,
            productivity_score INTEGER NOT NULL,
            notes TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()