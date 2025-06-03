from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout
from PySide6.QtCore import QTimer

from ui.warningsection import WarningSection
from ui.tabsection import TabSection
from ui.menusection import MenuSection

from modules.conflictDetector import ConflictDetector
from modules.backupOperations import BackupOperations
from modules.mediaPlayer import MediaPlayer

# Class for the main window, contains the objects for app contents
class MainWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()

        # Variables
        self.app = app
        self.conflict_detector = ConflictDetector()
        self.media_player = MediaPlayer()

        # Create app window
        self.setWindowTitle("Requirements Conflict Detection Software")

        # ____LAYOUT____
        # QMainWindow needs central widget to make layout work 
        central_widget = QWidget() 
        layout = QGridLayout()

        # ____WARNING SECTION____
        warning_widget = WarningSection(None, self.media_player)
        layout.addWidget(warning_widget, 1, 1)
        
        # ____TAB SECTION____
        tab_widget = TabSection(warning_widget,self.conflict_detector)
        warning_widget.set_tab_widget(tab_widget)
        layout.addWidget(tab_widget, 1, 0, 1, 1)

        # ___REQUIREMENT SECTION___
        # This section belongs under/with tab section
        # center_widget = RequirementSection()
        # layout.addWidget(center_widget, 1, 0)   

        # ____RETRIEVE BACKUP____
        # Codes to retrieve backup
        self.backup = BackupOperations(tab_widget)
        if self.backup.is_backup_empty() == True:
            tab_widget.add_requirement_tab(title="Requirement List")
        else:
            self.backup.retrieve_backup()

        # ____MENU SECTION____
        # Codes for the menu on the top part of the window
        self.menu = MenuSection(
            self, self.media_player, tab_widget,warning_widget,
            self.conflict_detector, self.backup)

        # Set column stretches
        layout.setColumnStretch(0, 3)  # main content area (tab section + requirement section)
        layout.setColumnStretch(1, 1)  # warning area

        # Set Layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget) 

        #____AUTO BACKUP____
        # Codes for automatic backup
        QTimer.singleShot(1000, self.backup.perform_backup)
        self.backup_timer = QTimer(self)
        self.backup_timer.timeout.connect(self.backup.perform_backup)
        self.backup_timer.start(1000*60*5) # 1000 ms * 60 sec * 5 min = 300,000 ms or 5 minute 

