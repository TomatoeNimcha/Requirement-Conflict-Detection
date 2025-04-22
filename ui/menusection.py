from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)

class MenuSection(QWidget):
    def __init__(self, window):
        self.window = window
        self.menu_bar = self.window.menuBar()

        self._create_menus()

    def _create_menus(self):
        settings_menu = self.menu_bar.addMenu("&Settings")
        settings_menu.addAction("Compare Lists")
        settings_menu.addAction("Merge Lists")
        settings_menu.addAction("Template")
        settings_menu.addAction("Import")
        settings_menu.addAction("Export")