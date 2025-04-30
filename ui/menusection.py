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
        filename, _ = QFileDialog.getOpenFileName(self, "Open Requirements", "", "JSON Files (*.json)")

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                title = data.get("title", "Untitled")
                author = data.get("author", "Unknown")
                requirements = data.get("requirementList", [])

                # Create new tab with imported data
                tab = RequirementSection(title, author)

                # Fill table with requirements
                tab.table.setRowCount(len(requirements))
                for row_index, req in enumerate(requirements):
                    req_id = req.get("requirementID", "")
                    req_text = req.get("requirement", "")
                    tab.table.setItem(row_index, 0, QTableWidgetItem(req_id))
                    tab.table.setItem(row_index, 1, QTableWidgetItem(req_text))

                self.tab_widget.insertTab(self.tab_widget.count() - 1, tab, title)
                self.tab_widget.setCurrentWidget(tab)

                QMessageBox.information(self, "Import Successful", f"Imported tab '{title}' with {len(requirements)} items.")

            except Exception as e:
                QMessageBox.critical(self, "Import Failed", f"Error: {e}")

    def exportJson(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save Requirements", "", "JSON Files (*.json)")

        if filename:
            current_widget = self.tab_widget.currentWidget()

            if isinstance(current_widget, RequirementSection):
                data = current_widget.to_dictionary()

                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)

                QMessageBox.information(self.window, "Exported", f"Exported current list to {filename}")
            else:
                QMessageBox.warning(self.window, "Export Error", "Error")


