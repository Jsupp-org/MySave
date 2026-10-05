from database.database import Database

class GoalRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def get_folder(self, name: str) -> tuple[int, float] | None:
        with self.database.connect() as conn:
            row = conn.execute(
                "SELECT id, goal_amount FROM savings_folders WHERE name = ?", (name,)
            ).fetchone()
        return row

    def save(self, folder_id: int, goal_amount: float) -> None:
        with self.database.connect() as conn:
            conn.execute(
                "UPDATE savings_folders SET goal_amount = ? WHERE id = ?",
                (goal_amount, folder_id),
            )