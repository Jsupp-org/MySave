from database.database import Database
from features.SavingsManagement.model import SavingsModel

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

    def get_history(self, folder_id: int) -> list[SavingsModel]:
        """Returns the folder's deposits and withdrawals, newest first.
        Dates are stored in UTC, so they are converted to local time here."""
        with self.database.connect() as conn:
            rows = conn.execute(
                "SELECT id, folder_id, transaction_type, amount, note, "
                "datetime(create_at, 'localtime') "
                "FROM savings_transac WHERE folder_id = ? ORDER BY id DESC",
                (folder_id,),
            ).fetchall()
        return [
            SavingsModel(
                id=row[0], folder_id=row[1], transaction_type=row[2],
                amount=row[3], note=row[4], create_at=row[5],
            )
            for row in rows
        ]
