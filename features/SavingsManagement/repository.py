from database.database import Database

class SavingsRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def get_folder(self, name: str) -> tuple[int, float] | None:
        with self.database.connect() as conn:
            row = conn.execute(
                "SELECT id, current_amount FROM savings_folders WHERE name = ?",
                (name,),
            ).fetchone()
            return row

    def record(self, folder_id: int, transaction_type: str, amount: float) -> int:
        change = amount if transaction_type == "deposit" else -amount

        with self.database.connect() as conn:
            conn.execute(
                "UPDATE savings_folders SET current_amount = current_amount + ? "
                "WHERE id = ?",
                (change, folder_id),
            )
            cursor = conn.execute(
                "INSERT INTO savings_transac (folder_id, transaction_type, amount ) "
                "VALUES (?, ?, ?)",
                (folder_id, transaction_type, amount)
            )
        return cursor.lastrowid
