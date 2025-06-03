from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QApplication,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton,QLineEdit,
    QHeaderView
)
from PySide6.QtCore import Qt, Signal, QObject, QTimer
from PySide6.QtGui import QColor, QBrush

from ui.warningsection import WarningSection

# Class for requirement list, author and title
class RequirementSection(QWidget):
    def __init__(self, warning_widget, conflict_detector, title="Default Title",author="Default Author"):
        super().__init__()

        # Variables
        self.warning_widget = warning_widget     
        self.title = title
        self.author = author
        self.conflict_detector = conflict_detector
        
        # Layout
        layout = QVBoxLayout()

        # Title
        self.title = QLineEdit(title)
        self.title.setStyleSheet("font-weight: bold; font-size: 16px; border: none;")
        self.title.setReadOnly(True)
        self.title.mouseDoubleClickEvent = lambda e: self.title.setReadOnly(False)
        self.title.editingFinished.connect(lambda: self.title.setReadOnly(True))
        layout.addWidget(self.title)

        # Author
        self.author = QLineEdit(author)
        self.author.setStyleSheet("font-weight: thin; font-size: 10px; border: none;")
        self.author.setReadOnly(True)
        self.author.mouseDoubleClickEvent = lambda e: self.author.setReadOnly(False)
        self.author.editingFinished.connect(lambda: self.author.setReadOnly(True))
        layout.addWidget(self.author)

        # Table
        self.table = QTableWidget(10, 3)
        self.table.setHorizontalHeaderLabels(["Requirement ID", "Requirement", "Notes"])
        self.table.setColumnWidth(0, 100) #ID
        self.table.setColumnWidth(1, 500) #Requirement
        #self.table.setColumnWidth(2, 100) #Attributes, useless because it stretches to the right anyways
        self.table.horizontalHeader().setStretchLastSection(True)    
        
        # Default Table Contents
        self.table.setItem(0, 0, QTableWidgetItem("REQ-001"))
        self.table.setItem(0, 1, QTableWidgetItem("The user can log in"))
        self.table.setItem(0, 2, QTableWidgetItem("Functional Requirement"))
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

    # Method for adding selected row
    def add_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.insertRow(selected + 1)
        else:
            self.table.insertRow(self.table.rowCount())

    # Method for removing selected row
    def remove_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)
        else:
            self.table.removeRow(self.table.rowCount())

    # Method for removing conflict row by passing a row into it  
    def remove_conflict_row(self, row):
        self.table.removeRow(row)

    # Method for updating requirement text of a row
    def update_row_text(self, row_index, new_text):
        table = self.table  
        if 0 <= row_index < table.rowCount():
            table.setItem(row_index, 1, QTableWidgetItem(new_text)) 

    # Method for updating requirement of any row and collumn
    def update_any_text(self, row, collumn, text):
        table = self.table 
        if 0 <= row < table.rowCount():
            table.setItem(row, collumn, QTableWidgetItem(text)) 

    # Getter for requirement table content
    def get_table_contents(self):
        table_contents = []

        for row in range(self.table.rowCount()):
            id_item = self.table.item(row, 0)
            req_item = self.table.item(row, 1)
            att_item = self.table.item(row, 2)

            req_id = id_item.text().strip() if id_item else ""
            req_text = req_item.text().strip() if req_item else ""
            req_att = att_item.text().strip() if att_item else ""

            if req_id or req_text:
                table_contents.append((row, req_id, req_text, req_att))

        return table_contents
    
    # Getter for requirement list title
    def get_title(self):
        return self.title.text()
    
    # Getter for requirement listauthor name
    def get_author(self):
        return self.author.text()
    
    # Getter for total requirement list row
    def get_total_row(self):
        return self.table.rowCount()

    # Getter for conflicts found in the requirement list
    def get_conflict_from_table(self):
        # Does not show due to execution speed but will still be left here
        self.warning_widget.add_status("Detecting conflicts . . . ")
        
        table_contents = self.get_table_contents()
        conflicts = self.conflict_detector.detect_conflict(table_contents)

        return conflicts

   # Method to search something in the requirement list
    def search_table(self, text_to_find):
        table = self.table 
        matches = []

        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and text_to_find.lower() in item.text().lower():
                    matches.append((row, col))

        return matches

    # Method to clear highlights in the table
    def clear_highlights(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QColor(Qt.transparent))

    # Method to highlight row with chosen color
    def highlight_rows(self, rows, color):
        for entry in rows:
            if isinstance(entry, tuple) and len(entry) == 2:
                # Pair of rows (e.g., redundancy)
                row1, row2 = entry
                for col in range(self.table.columnCount()):
                    item1 = self.table.item(row1, col)
                    item2 = self.table.item(row2, col)
                    if item1:
                        item1.setBackground(QColor(color))
                    if item2:
                        item2.setBackground(QColor(color))
            elif isinstance(entry, int):
                # Single row 
                for col in range(self.table.columnCount()):
                    item = self.table.item(entry, col)
                    if item:
                        item.setBackground(QColor(color))
                
    # Method to show conflicts in the list, theres two of these due to it kept breaking when i try to merge them
    def show_conflicts(self):
        self.clear_highlights()

        conflicts = self.get_conflict_from_table()

        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["redundancy"], 2), "fireBrick")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["contradiction"], 2), "orangeRed")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["similarity"], 2), "goldenRod")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["ambiguity"], 1), "indigo")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["incomplete"], 1), "fireBrick")


        self.warning_widget.conflict_warning(conflicts)

    def show_combined_conflicts(self, conflicts):
        self.clear_highlights()

        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["redundancy"], 2), "fireBrick")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["contradiction"], 2), "orangeRed")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["similarity"], 2), "goldenRod")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["ambiguity"], 1), "indigo")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["incomplete"], 1), "fireBrick")

        self.warning_widget.conflict_warning(conflicts)




        
    

    
