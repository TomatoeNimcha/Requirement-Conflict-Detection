# ui/requirement_table_widget.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)

class RequirementSection(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Label
        title = QLabel("Requirement Table")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        # Table
        self.table = QTableWidget(5, 2)
        self.table.setHorizontalHeaderLabels(["Requirement", "Description"])
        self.table.setColumnWidth(1, 400)

        # Example Table Contents
        self.table.setItem(0, 0, QTableWidgetItem("REQ-001"))
        self.table.setItem(0, 1, QTableWidgetItem("User can log in"))
        layout.addWidget(self.table)

        # Buttons
        button_layout = QHBoxLayout()
        add_button = QPushButton("+ Add Row")
        remove_button = QPushButton("- Remove Row")
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)
        layout.addLayout(button_layout)

        # Logic
        add_button.clicked.connect(self.add_row)
        remove_button.clicked.connect(self.remove_row)

        self.setLayout(layout)

    def add_row(self):
        self.table.insertRow(self.table.rowCount())

    def remove_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)