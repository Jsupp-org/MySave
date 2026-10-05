from database.database import Database
from features.helpers import parse_amount
from features.SavingsManagement.model import SavingsModel
from features.SavingsManagement.repository import SavingsRepository

class SavingsService:
    def __init__(self, database: Database) -> None:
        self.repository = SavingsRepository(database)

    def find_folder(self, name: str) -> tuple[int, float]:
        folder = self.repository.get_folder(name.strip())
        if folder is None:
            raise ValueError("Folder not found.")
        return folder

    def add_savings(self, folder_name: str, amount_text: str) -> SavingsModel:
        folder_id, _ = self.find_folder(folder_name)
        amount = parse_amount(amount_text)
        transaction = SavingsModel(folder_id, "deposit", amount)
        transaction.id = self.repository.record(folder_id, "deposit", amount)
        return transaction

    def subtract_savings(self, folder_name: str, amount_text: str) -> SavingsModel:
        folder_id, current_amount = self.find_folder(folder_name)
        amount = parse_amount(amount_text)
        transaction = SavingsModel(folder_id, "withdraw", amount)
        if amount > current_amount:
            raise ValueError(
                f"Insufficient balance. '{folder_name.strip()}' only has P{current_amount:,.2f}."
            )
        transaction.id = self.repository.record(folder_id, "withdraw", amount)
        return transaction