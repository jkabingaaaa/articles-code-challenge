import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent 

def get_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    with get_connection() as conn:
        with open(Path(__file__).parent / "schema.sql") as f:
            conn.executescript(f.read())