import sqlite3

DB_NAME = "students.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            math_marks REAL NOT NULL,
            science_marks REAL NOT NULL,
            english_marks REAL NOT NULL,
            average REAL NOT NULL,
            result TEXT NOT NULL,
            grade TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()