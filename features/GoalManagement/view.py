from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import *

from features.GoalManagement.service import GoalService
from features.SavingsFolderManagement.service import SavingsFolderService

class GoalView(QWidget):
    data_changed = pyqtSignal()

    def __init__(self, service: GoalService, folder_service: SavingsFolderService) -> None:
        super().__init__()
        self.service = service
        self.folder_service = folder_service
        self.build_ui()
        self.refresh()

    def build_ui(self) -> None:
        layout =QVBoxLayout(self)

        layout.addWidget(QLabel("Folder:"))
        self.folder_combo = QComboBox()
        self.folder_combo.currentTextChanged.connect(self.show_current_goal)
        layout.addWidget(self.folder_combo)

        self.current_goal_label = QLabel("Current goal: -")
        layout.addWidget(self.current_goal_label)

        layout.addWidget(QLabel("Goal amount:"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("e.g. 5000")
        layout.addWidget(self.amount_input)

        button_row = QHBoxLayout()
        set_button = QPushButton("Set Goal")
        set_button.clicked.connect(self.set)
        button_row.addWidget(set_button)

        update_button = QPushButton("Update Goal")
        update_button.clicked.connect(self.update)
        button_row.addWidget(update_button)
        layout.addLayout(button_row)

        layout.addStretch()

    def set(self) -> None:
        name = self.folder_combo.currentText()
        try:
            goal = self.service.create_goal(name, self.amount_input.text())
        except ValueError as error:
            self.warn(str(error))
            return
        QMessageBox.information(
            self, "Goal Set", f"Goal of P{goal.goal_amount:,.2f} has been set for '{name}'."
        )
        self.amount_input.clear()
        self.data_changed.emit()

    def update(self) -> None:
        name = self.folder_combo.currentText()
        try:
            goal = self.service.update_goal(name, self.amount_input.text())
        except ValueError as error:
            self.warn(str(error))
            return
        QMessageBox.information(
            self, "Goal Updated", f"Goal for '{name}' has been updated to P{goal.goal_amount:,.2f}."
        )
        self.amount_input.clear()
        self.data_changed.emit()

    def show_current_goal(self, name: str) -> None:
        if not name:
            self.current_goal_label.setText("Current goal: -")
            return
        try:
            folder = self.folder_service.view_folder(name)
        except ValueError:
            self.current_goal_label.setText("Current goal: -")
            return
        if folder.goal_amount == 0:
            self.current_goal_label.setText("Current goal: not set")
        else:
            self.current_goal_label.setText(f"Current goal: P{folder.goal_amount:,.2f}")

    def refresh(self) -> None:
        selected = self.folder_combo.currentText()
        self.folder_combo.clear()
        self.folder_combo.addItems([f.name for f in self.folder_service.view_all()])
        index = self.folder_combo.findText(selected)
        if index >= 0:
             self.folder_combo.setCurrentIndex(index)
        self.show_current_goal(self.folder_combo.currentText())


    def warn(self, message: str) -> None:
            QMessageBox.warning(self, "Error", message)
