from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QGridLayout, QLabel,
    QTableWidget,QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout)

from ui.requirementsection import RequirementSection
from ui.warningsection import WarningSection

class MainWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Requirements Conflict Detection Software")

        # Layout
        #For some reason QMainWindow need central widget to make layout work 
        central_widget = QWidget() 
        layout = QGridLayout()

        # MenuBar and Menus
        menu_bar = self.menuBar()

        settings_menu = menu_bar.addMenu("&Settings")
        compare_action = settings_menu.addAction("Compare Lists")
        merge_action = settings_menu.addAction("Merge Lists")
        template_action = settings_menu.addAction("Template")
        import_action = settings_menu.addAction("Import")
        export_action = settings_menu.addAction("Export")
        
        # --- HEADER TABS ---
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("QTabBar::tab { height: 30px; padding: 8px; }")
        layout.addWidget(tab_widget, 1, 0, 1, 1)  # center area only

        # Add requirement table into each tabs
        tab1 = RequirementSection()
        tab2 = RequirementSection()

        tab_widget.addTab(tab1, "List 1")
        tab_widget.addTab(tab2, "List 2")


        # --- CENTER REQUIREMENT TABLE AREA ---
        # center_widget = RequirementSection()
        # layout.addWidget(center_widget, 1, 0)
        

        # --- WARNING AREA  ---
        warning_widget = WarningSection()
        layout.addWidget(warning_widget, 1, 1)

        # Set column stretches: left wider than right
        layout.setColumnStretch(0, 3)  # main content area
        layout.setColumnStretch(1, 1)  # warning area

        # Set Layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

