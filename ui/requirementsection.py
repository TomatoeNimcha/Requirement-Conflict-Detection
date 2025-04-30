from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)
from PySide6.QtCore import Qt

from PySide6.QtGui import QColor, QBrush

import json
from modules.spacyImplementation import SpacyImplementation
from ui.warningsection import WarningSection

class RequirementSection(QWidget):
    def __init__(self,title="Default Title",author="Default Author", warning=None):
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

        check_button = QPushButton("Check for Conflicts")
        button_layout.addWidget(check_button)

        layout.addLayout(button_layout)

        # Logic
        add_button.clicked.connect(self.add_row)
        remove_button.clicked.connect(self.remove_row)
        check_button.clicked.connect(self.check_conflict)

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

            # Skip empty rows
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


    def check_conflict(self):
        spacy_checker = SpacyImplementation()
        conflicts = []

        # First, clear all previous background highlights
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QBrush(Qt.NoBrush))
                    #no method of removing background so this is the roundabout way to do it apparently

        # Collect all requirements from the table
        requirements = []
        for row in range(self.table.rowCount()):
            id_item = self.table.item(row, 0)
            req_item = self.table.item(row, 1)

            if id_item and req_item:
                req_id = id_item.text().strip()
                req_text = req_item.text().strip()

                if req_id and req_text:
                    requirements.append((row, req_id, req_text))

        # Compare each requirement to every other
        for i in range(len(requirements)):
            for j in range(i + 1, len(requirements)):
                row1, id1, text1 = requirements[i]
                row2, id2, text2 = requirements[j]

                if spacy_checker.similarityCheck(text1, text2):
                    conflicts.append((row1, row2))

        # Highlight conflicting rows
        for row1, row2 in conflicts:
            for col in range(self.table.columnCount()):
                item1 = self.table.item(row1, col)
                item2 = self.table.item(row2, col)
                if item1:
                    item1.setBackground(QColor("red")) 
                if item2:
                    item2.setBackground(QColor("red"))

