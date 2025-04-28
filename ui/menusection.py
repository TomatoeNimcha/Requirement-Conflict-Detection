from PySide6.QtWidgets import (
    QWidget, QFileDialog, QMenuBar, QMessageBox,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)

import json
from ui.requirementsection import RequirementSection

class MenuSection(QWidget):
    def __init__(self, window, tab_widget):
        super().__init__()
        self.window = window
        self.tab_widget = tab_widget
        self.menu_bar = self.window.menuBar()

        self.create_menus()

    def create_menus(self):
        settings_menu = self.menu_bar.addMenu("&Options")

        compare_action = settings_menu.addAction("Compare Lists")
        merge_action = settings_menu.addAction("Merge Lists")
        template_action = settings_menu.addAction("Template")
        import_action = settings_menu.addAction("Import")
        export_action = settings_menu.addAction("Export")

        # Connect actions to methods
        compare_action.triggered.connect(self.compare)
        merge_action.triggered.connect(self.merge)
        template_action.triggered.connect(self.template)
        import_action.triggered.connect(self.importJson)
        export_action.triggered.connect(self.exportJson)

    def compare(self):
        QMessageBox.information(self, "Compare", "Logic here.")

    def merge(self):
        QMessageBox.information(self, "Merge", "Logic here.")

    def template(self):
        QMessageBox.information(self, "Template", "Logic here.")

    def importJson(self):
        QMessageBox.information(self, "Import Json", "Logic here.")

    def exportJson(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Requirements", "", "JSON Files (*.json)")

        if filename:
            all_data = []

            for i in range(self.tab_widget.count()):
                widget = self.tab_widget.widget(i)
                if isinstance(widget, RequirementSection):
                    all_data.append(widget.to_dictionary())

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=4, ensure_ascii=False)

            QMessageBox.information(self.window, "Exported", f"Exported {len(all_data)} lists to {filename}")


