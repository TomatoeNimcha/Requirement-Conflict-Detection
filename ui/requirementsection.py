from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton,QLineEdit
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QColor, QBrush

from ui.warningsection import WarningSection
from ui.tagsection import TagSection

class RequirementSection(QWidget):
    def __init__(self, warning_widget, conflict_detector, title="Default Title",author="Default Author"):
        super().__init__()

        # Declare variables so it is editable later on
        self.warning_widget = warning_widget     
        self.title = title
        self.author = author
        self.conflict_detector = conflict_detector
        
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
        self.table.setHorizontalHeaderLabels(["Requirement ID", "Requirement", "Attributes"])
        self.table.setColumnWidth(0, 100) #ID
        self.table.setColumnWidth(1, 325) #Requirement
        #self.table.setColumnWidth(2, 100) #Attributes, useless because it stretches to the right anyways
        self.table.horizontalHeader().setStretchLastSection(True)
        
        tags = [("important", "#ff6b6b"), ("non-functional", "#0d6efd")]
        
        # Example Table Contents
        self.table.setItem(0, 0, QTableWidgetItem("REQ-001"))
        self.table.setItem(0, 1, QTableWidgetItem("User can log in"))
        self.table.setCellWidget(0, 2, TagSection(tags))
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
    
    def remove_conflict_row(self, row):
        self.table.removeRow(row)

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
    
    def get_title(self):
        return self.title.text()
    
    def get_author(self):
        return self.author.text()

    def get_conflict_from_table(self):
        table_contents = self.get_table_contents()
        conflicts = self.conflict_detector.detect_conflict(table_contents)

        return conflicts

    
    def clear_highlights(self):
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(QColor(Qt.transparent))

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
        self.clear_highlights()

        conflicts = self.get_conflict_from_table()

        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["redundancy"]), "red")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["contradiction"]), "orange")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["similarity"]), "yellow")

        self.warning_widget.conflict_warning(conflicts)


    def show_combined_conflicts(self, conflicts):
        self.clear_highlights()

        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["redundancy"]), "red")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["contradiction"]), "orange")
        self.highlight_rows(self.conflict_detector.extract_rows(conflicts["similarity"]), "yellow")

        self.warning_widget.conflict_warning(conflicts)




        
    

    
