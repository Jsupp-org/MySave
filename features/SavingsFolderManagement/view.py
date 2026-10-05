from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import *

from features.SavingsFolderManagement.service import SavingsFolderService

class SavingsFolderView(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, service: SavingsFolderService):
        super().__init__()
        self.service = service
        self.build_ui()
        self.refresh()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Folder", "Balance", "Goal"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

        self.total_Label = QLabel()
        layout.addWidget(self.total_Label)

        create_row = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("New folder name")
        create_row.addWidget(self.name_input)
        create_button = QPushButton("Create Folder")
        create_button.clicked.connect(self.on_create)
        create_row.addWidget(create_button)
        layout.addLayout(create_row)


        action_row = QHBoxLayout()
        view_button = QPushButton("View Selected Folder")
        view_button.clicked.connect(self.on_view)
        action_row.addWidget(view_button)
        
        delete_button = QPushButton("Delete Selected Folder")
        delete_button.clicked.connect(self.on_delete)
        action_row.addWidget(delete_button)
        layout.addLayout(action_row)    
 

    def on_create(self) -> None:
        try:
            folder = self.service.create_folder(self.name_input.text())
        except ValueError as error:
            self.warn(str(error))
            return
        self.name_input.clear()
        QMessageBox.information(self, "Folder Created", f"Folder '{folder.name}' has been created.")
        self.data_changed.emit()

    def on_view(self) -> None:
        name = self.selected_name()
        if name is None:
            self.warn("No folder selected.")
            return
        try:
            folder = self.service.view_folder(name)
        except ValueError as error:
            self.warn(str(error))
            return
        QMessageBox.information(
            self, "Folder", f"{folder.name} balance: P{folder.current_amount:,.2f}"
        )


    def on_delete(self) -> None:
        name = self.selected_name()
        if name is None:
            self.warn("Please select a folder first.")
            return
        try:
            self.service.delete_folder(name)
        except ValueError as error:
            self.warn(str(error))
            return
        QMessageBox.information(self, "Folder Deleted", f"Folder '{name}' has been deleted.")
        self.data_changed.emit()

    def selected_name(self) -> str | None:
        row = self.table.currentRow()
        if row < 0:
            return None
        return self.table.item(row, 0).text()

    def refresh(self) -> None:
        folders = self.service.view_all()
        self.table.setRowCount(len(folders))
        for row, folder in enumerate(folders):
            self.table.setItem(row, 0, QTableWidgetItem(folder.name))
            self.table.setItem(row, 1, QTableWidgetItem(f"P{folder.current_amount:,.2f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"P{folder.goal_amount:,.2f}"))
        self.total_Label.setText(f"Total savings: P{self.service.get_total_savings():,.2f}")

    def warn(self, message: str) -> None:
        QMessageBox.warning(self, "Warning", message)

