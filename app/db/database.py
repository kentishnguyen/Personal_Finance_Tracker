import json
>>>>>>> dev
import sqlite3
from pathlib import Path

DB_PATH = Path("receipts.db")
SCHEMA_PATH = Path("app/db/schema.sql")

# this function returns 
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initializing a database, this should get called on startup
def init_db() -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_db_connection() as conn:
        conn.executescript(schema)
        conn.commit()
