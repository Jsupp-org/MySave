from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import *

from features.SavingsFolderManagement.service import SavingsFolderService
from features.SavingsManagement.service import SavingsService

class SavingsView(QWidget):
    data_changed = pyqtSignal()
    
    def __init__(self, service: SavingsService, folder_service: SavingsFolderService) -> None:
        super().__init__()
        self.service = service
        self.folder_service = folder_service
        self.build_ui()
        self.refresh()

    def build_ui(self) -> None:
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Folder:"))
        self.folder_combo = QComboBox()
        layout.addWidget(self.folder_combo)

        layout.addWidget(QLabel("Amount:"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("e.g. 500")
        layout.addWidget(self.amount_input)

        button_row = QHBoxLayout()
        add_button = QPushButton("Add Savings")
        add_button.clicked.connect(self.add)
        button_row.addWidget(add_button)

        subtract_button = QPushButton("Subtract Savings")
        subtract_button.clicked.connect(self.subtract)
        button_row.addWidget(subtract_button)
        layout.addLayout(button_row)

        layout.addStretch()

    def add(self) -> None:
        try:
            transaction = self.service.add_savings(
                self.folder_combo.currentText(), self.amount_input.text()
            )
        except ValueError as error:
            self.warn(str(error))
            return
        QMessageBox.information(
            self, "Savings Added",
            f"P{transaction.amount:,.2f} has been added to your savings in {self.folder_combo.currentText()}'.",
        )
        self.amount_input.clear()
        self.data_changed.emit()

    def subtract(self) -> None:
        try:
            transaction = self.service.subtract_savings(
                self.folder_combo.currentText(), self.amount_input.text()
            )
        except ValueError as error:
            self.warn(str(error))
            return
        QMessageBox.information(
            self, "Savings Subtracted", 
            f"P{transaction.amount:,.2f} has been subtracted from your savings in {self.folder_combo.currentText()}'.",
        )
        self.amount_input.clear()
        self.data_changed.emit()

    def refresh(self) -> None:
        selected = self.folder_combo.currentText()
        self.folder_combo.clear()
        self.folder_combo.addItems([f.name for f in self.folder_service.view_all()])
        index = self.folder_combo.findText(selected)
        if index >= 0:
            self.folder_combo.setCurrentIndex(index)

    def warn(self, message: str) -> None:
        QMessageBox.warning(self, "Error", message)
