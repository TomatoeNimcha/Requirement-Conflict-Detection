from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)
from PySide6.QtCore import Qt

from PySide6.QtGui import QColor, QBrush


from modules.conflictDetector import ConflictDetector
from ui.warningsection import WarningSection

class RequirementSection(QWidget):
    def __init__(self,title="Default Title",author="Default Author", warning_section=None):
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
        self.table.setHorizontalHeaderLabels(["Requirement ID", "Requirement", "Attributes"])
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
        check_button.clicked.connect(self.show_conflicts)

        self.setLayout(layout)

    def add_row(self):
        self.table.insertRow(self.table.rowCount())

    def remove_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)

    def get_table_contents(self):
        table_contents = []

        for row in range(self.table.rowCount()):
            id_item = self.table.item(row, 0)
            req_item = self.table.item(row, 1)

            req_id = id_item.text().strip() if id_item else ""
            req_text = req_item.text().strip() if req_item else ""

            if req_id or req_text:
                table_contents.append((row, req_id, req_text))

        return table_contents
    
    def get_title(self):
        return self.title
    
    def get_author(self):
        return self.author

    def get_conflict_from_table(self):
        conflict_detector = ConflictDetector()

        table_contents = self.get_table_contents()
        conflicts = conflict_detector.detect_conflict(table_contents)

        return conflicts

    def highlight_rows(self, row_pairs, color):
        for row1, row2 in row_pairs:
            for col in range(self.table.columnCount()):
                item1 = self.table.item(row1, col)
                item2 = self.table.item(row2, col)
                if item1:
                    item1.setBackground(QColor(color))
                if item2:
                    item2.setBackground(QColor(color))


    def show_conflicts(self):
        conflicts = self.get_conflict_from_table()

        self.highlight_rows(conflicts["similarity"], "yellow")
        self.highlight_rows(conflicts["redundancy"], "red")
        self.highlight_rows(conflicts["contradiction"], "orange")

        
    

    
