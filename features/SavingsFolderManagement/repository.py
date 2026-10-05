from database.database import Database
from features.SavingsFolderManagement.model import SavingsFolderModel

class SavingsFolderRepository:
    def __init__ (self, database: Database) -> None:
        self.database = database

    def add_folder(self, folder: SavingsFolderModel) -> SavingsFolderModel:
        with self.database.connect() as conn:
            cursor = conn.execute(
                "INSERT INTO savings_folders (name, goal_amount, current_amount)"
                "VALUES (?, ?, ?)",
                (folder.name, folder.goal_amount, folder.current_amount),
            )
            folder.id = cursor.lastrowid
        return folder

    def get_folder(self, name: str) -> SavingsFolderModel | None:
        with self.database.connect() as conn:
            row = conn.execute(
                "SELECT id, name, goal_amount, current_amount "
                "FROM savings_folders WHERE name = ?",
                (name,),
            ).fetchone()
        return self.to_folder(row) if row else None

    def get_all(self) -> list[SavingsFolderModel]:
        with self.database.connect() as conn:
            rows = conn.execute(
                "SELECT id, name, goal_amount, current_amount "
                "FROM savings_folders ORDER BY name"
            ).fetchall()
        return [self.to_folder(row) for row in rows]

    def delete(self, folder_id: int) -> None:
        with self.database.connect() as conn:
            conn.execute("DELETE FROM savings_folders WHERE id = ?", (folder_id,))

    @staticmethod
    def to_folder(row) -> SavingsFolderModel:
        return SavingsFolderModel(
            id=row[0], name=row[1], goal_amount=row[2], current_amount=row[3]
        )