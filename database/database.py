import sqlite3
from pathlib import Path

class Database:
    def __init__(self, database_path: str | Path | None = None) -> None:
        if database_path is None:
            database_path = Path(__file__).parent / "savings.db"
        self.database_path = Path(database_path)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.database_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_table(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS savings_folders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    goal_amount REAL NOT NULL DEFAULT 0,
                    current_amount REAL NOT NULL DEFAULT 0,
                    create_at TEXT NOT NULL DEFAULT (datetime('now'))
                );
                    
                CREATE TABLE IF NOT EXISTS savings_transac(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    folder_id INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('deposit', 'withdraw')),
                    amount REAL NOT NULL CHECK (amount > 0),
                    note TEXT,
                    create_at TEXT NOT NULL DEFAULT (datetime('now')),
                    FOREIGN KEY (folder_id) REFERENCES savings_folders(id) ON DELETE CASCADE
                );
                """
            )