import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget

from database.database import Database
from features.SavingsFolderManagement.service import SavingsFolderService
from features.SavingsFolderManagement.view import SavingsFolderView
from features.SavingsManagement.service import SavingsService
from features.SavingsManagement.view import SavingsView
from features.GoalManagement.service import GoalService
from features.GoalManagement.view import GoalView


class MainWindow(QMainWindow):
    def __init__(self, database: Database) -> None:
        super().__init__()
        self.setWindowTitle("MySave - Personal Savings Tracker")
        self.resize(650, 480)

        folder_service = SavingsFolderService(database)
        savings_service = SavingsService(database)
        goal_service = GoalService(database)

        self.folder_view = SavingsFolderView(folder_service)
        self.savings_view = SavingsView(savings_service, folder_service)
        self.goal_view = GoalView(goal_service, folder_service)
        self.views = [self.folder_view, self.savings_view, self.goal_view]
        
        tabs = QTabWidget()
        tabs.addTab(self.folder_view, "Folders")
        tabs.addTab(self.savings_view, "Savings")
        tabs.addTab(self.goal_view, "Goals")
        self.setCentralWidget(tabs)

        for view in self.views:
            view.data_changed.connect(self.refresh_all)

    def refresh_all(self) -> None:
        for view in self.views:
            view.refresh()

if __name__ == "__main__":
    database = Database()
    database.create_table()

    app = QApplication(sys.argv)
    window = MainWindow(database)
    window.show()
    sys.exit(app.exec())