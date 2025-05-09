from PySide6.QtWidgets import (
    QWidget, QFileDialog, QMenuBar, QMessageBox,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton
)

from ui.tabsection import TabSection
from ui.requirementsection import RequirementSection
from modules.fileOperations import FileOperations

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
        compare_action.triggered.connect(self.compare_requirements)
        merge_action.triggered.connect(self.merge_requirements)
        template_action.triggered.connect(self.requirement_template)
        import_action.triggered.connect(self.import_requirements)
        export_action.triggered.connect(self.export_requirements)

    def compare_requirements(self):
        QMessageBox.information(self, "Compare", "Logic here.")

    def merge_requirements(self):
        QMessageBox.information(self, "Merge", "Logic here.")

    def requirement_template(self):
        QMessageBox.information(self, "Template", "Logic here.")

    def import_requirements(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Import Requirements", "", "JSON Files (*.json)")

        if filepath:
            try:
                data = FileOperations.read_file(filepath)
                title, author, requirements = FileOperations.dictionary_to_table(data)

                tab = RequirementSection(title, author)
                tab.table.setRowCount(len(requirements))
                for row, item in enumerate(requirements):
                    tab.table.setItem(row, 0, QTableWidgetItem(item.get("requirementID", "")))
                    tab.table.setItem(row, 1, QTableWidgetItem(item.get("requirement", "")))

                # MAY HAVE SIMILAR ISSUE IN TABSECTION, ADD TAB
                self.tab_widget.insertTab(self.tab_widget.count() - 1, tab, title)
                self.tab_widget.setCurrentWidget(tab)

                QMessageBox.information(self, "Import Successful", f"Imported {len(requirements)} requirements.")

            except Exception as e:
                QMessageBox.critical(self, "Import Failed", f"Error: {e}")   

    def export_requirements(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Requirements", "", "JSON Files (*.json)")

        if filepath:
            widget = self.tab_widget.currentWidget()
            if isinstance(widget, RequirementSection):
                data = FileOperations.table_to_dictionary(widget.title, widget.author, widget.get_table_contents())
                FileOperations.write_file(filepath, data)
                QMessageBox.information(self, "Export Successful", f"Exported to {filepath}")
            else:
                QMessageBox.warning(self, "Export Error", "Not a requirement tab!")
        


