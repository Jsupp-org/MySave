from database.database import Database
from features.GoalManagement.model import GoalModel
from features.GoalManagement.repository import GoalRepository
from features.helpers import parse_amount

class GoalService:
    def __init__(self, database: Database) -> None:
        self.repository = GoalRepository(database)

    def create_goal(self, folder_name: str, amount_text: str) -> GoalModel:
        folder_id, _ = self.find_folder(folder_name)
        goal = GoalModel(folder_id, parse_amount(amount_text))
        self.repository.save(goal.folder_id, goal.goal_amount)
        return goal

    def update_goal(self, folder_name: str, amount_text: str) -> GoalModel:
        folder_id, current_goal = self.find_folder(folder_name)
        if current_goal == 0:
            raise ValueError("This folder does not have a goal set yet.")
        goal = GoalModel(folder_id, parse_amount(amount_text))
        self.repository.save(goal.folder_id, goal.goal_amount)
        return goal

    def find_folder(self, name: str) -> tuple[int, float]:
        folder = self.repository.get_folder(name.strip())
        if folder is None:
            raise ValueError("Folder not found.")
        return folder