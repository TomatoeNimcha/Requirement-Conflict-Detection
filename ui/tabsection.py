from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QTabWidget, QWidget, QInputDialog
)

from ui.requirementsection import RequirementSection

class TabSection(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("QTabBar::tab { height: 30px; padding: 8px; }")
        self.setTabsClosable(False)

        # Add initial tabs
        self.add_requirement_tab("List 2")
        self.add_requirement_tab("List 1")

        # Add "+" tab
        self.plus_tab = QWidget()
        self.addTab(self.plus_tab, "+")

        # Watch for tab changes
        self.currentChanged.connect(self.user_add_requirement_tab)


    def user_add_requirement_tab(self, index):
        if self.tabText(index) == "+":
            # 1. Ask for tab name
            name, ok = QInputDialog.getText(self, "New Tab", "Enter name for this requirement list:")

            if not ok or not name.strip():
                self.setCurrentIndex(0)            
            else:
                self.add_requirement_tab(name)


    # ISSUE : THIS WONT WORK UNLESS THERES AN INITIAL TAB BEFORE
    def add_requirement_tab(self, title=None, author=None):
        index = self.count() - 1  # always insert before "+" tab
        tab_name = title if title else f"List {index + 1}"
        tab = RequirementSection(tab_name)
        self.insertTab(index, tab, tab_name)
        self.setCurrentIndex(index)

