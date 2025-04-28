from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)

import json

class RequirementSection(QWidget):
    def __init__(self,title="Default Title",author="Default Author"):
        super().__init__()

        # Declare variables so it is editable later on
        self.title = title
        self.author = author

        layout = QVBoxLayout()

        # Label Title
        title = QLabel(title)
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        # Label Author
        author = QLabel(author)
        author.setStyleSheet("font-weight: thin; font-size: 10px;")
        layout.addWidget(author)

        # Table
        self.table = QTableWidget(5, 2)
        self.table.setHorizontalHeaderLabels(["Requirement ID", "Requirement"])
        self.table.horizontalHeader().setStretchLastSection(True)

        # Example Table Contents
        self.table.setItem(0, 0, QTableWidgetItem("REQ-001"))
        self.table.setItem(0, 1, QTableWidgetItem("User can log in"))
        self.table.setItem(1, 0, QTableWidgetItem("REQ-002"))
        self.table.setItem(1, 1, QTableWidgetItem("User can log out"))
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

    def to_dictionary(self):
        requirementList = []

        for row in range(self.table.rowCount()):
            requirementID_item = self.table.item(row, 0)
            requirement_item = self.table.item(row, 1)

            requirementID = requirementID_item.text() if requirementID_item else ""
            requirement = requirement_item.text() if requirement_item else ""

            # Skip empty rows (optional)
            if requirementID.strip() or requirement.strip():
                requirementList.append({
                    "requirementID": requirementID,
                    "requirement": requirement
                })

        return {
            "title": self.title,
            "author": self.author,
            "requirementList": requirementList
        }