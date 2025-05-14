from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QGridLayout, QLabel,
    QTableWidget,QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout)

from ui.requirementsection import RequirementSection
from ui.warningsection import WarningSection
from ui.tabsection import TabSection
from ui.menusection import MenuSection

class MainWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Requirements Conflict Detection Software")

        # ____LAYOUT____
        #For some reason QMainWindow need central widget to make layout work 
        central_widget = QWidget() 
        layout = QGridLayout()

        # ____WARNING SECTION____
        warning_widget = WarningSection()
        layout.addWidget(warning_widget, 1, 1)
        
        # ____TAB SECTION____
        tab_widget = TabSection(warning_widget)
        layout.addWidget(tab_widget, 1, 0, 1, 1)

        # ____MENU SECTION____
        self.menu = MenuSection(self,tab_widget)


        # --- CENTER REQUIREMENT TABLE AREA ---
        # center_widget = RequirementSection()
        # layout.addWidget(center_widget, 1, 0)   


        # Set column stretches: left wider than right
        layout.setColumnStretch(0, 3)  # main content area
        layout.setColumnStretch(1, 1)  # warning area

        # Set Layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

