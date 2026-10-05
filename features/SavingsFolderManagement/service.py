from database.database import Database
from features.SavingsFolderManagement.model import SavingsFolderModel
from features.SavingsFolderManagement.repository import SavingsFolderRepository

class SavingsFolderService:
    def __init__(self, database: Database) -> None:
        self.repository = SavingsFolderRepository(database)

    def create_folder(self, name: str) -> SavingsFolderModel:
        folder = SavingsFolderModel(name=name)
        if self.repository.get_folder(folder.name) is not None:
            raise ValueError("Folder name already exists.")
        return self.repository.add_folder(folder)

    def view_folder(self, name: str) -> SavingsFolderModel:
        folder = self.repository.get_folder(name.strip())
        if folder is None:
           raise ValueError("Folder not found.")
        return folder

    def view_all(self) -> list[SavingsFolderModel]:
        return self.repository.get_all()

    def delete_folder(self, name: str) -> None:
        folder = self.view_folder(name)
        if folder.current_amount != 0:
            raise ValueError(
                f"Cannot delete '{folder.name}'. Balance must be P0.00"
                f"(cuurently P{folder.current_amount:,.2f}).")
        self.repository.delete(folder.id)

    def get_total_savings(self) -> float:
        return sum(folder.current_amount for folder in self.repository.get_all())