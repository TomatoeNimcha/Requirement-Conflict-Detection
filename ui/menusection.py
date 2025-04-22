from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)

class MenuSection(QWidget):
    def __init__(self, window):
        self.window = window
        self.menu_bar = self.window.menuBar()

        self.create_menus()

    def create_menus(self):
        settings_menu = self.menu_bar.addMenu("&Settings")
        settings_menu.addAction("Compare Lists")
        settings_menu.addAction("Merge Lists")
        settings_menu.addAction("Template")
        settings_menu.addAction("Import")
        settings_menu.addAction("Export")

        list_menu = self.menu_bar.addMenu("&List")
        list_menu.addAction("Merge")