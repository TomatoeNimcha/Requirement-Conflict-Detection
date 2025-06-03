from PySide6.QtWidgets import (
    QWidget, QFileDialog, QMessageBox, QTableWidgetItem,
    QDialog, QFormLayout, QLineEdit, QSpinBox, QDialogButtonBox, 
    QInputDialog, QFontDialog 
)

from ui.requirementsection import RequirementSection
from modules.fileOperations import FileOperations
from data.template import template
import qdarktheme

# Class for the menus on the top part of the app
class MenuSection(QWidget):
    def __init__(self, window, media_player, tab_widget, warning_widget, conflict_detector, backup):
        super().__init__()

        # Variables
        self.window = window
        self.media_player = media_player
        self.tab_widget = tab_widget
        self.warning_widget = warning_widget
        self.conflict_detector = conflict_detector
        self.backup = backup
        self.menu_bar = self.window.menuBar()
        self.sound_action = None

        self.create_menus() # Calling create menu method

    # Method to create menu options for the main window
    def create_menus(self):

        # Create menu actions
        #___FILE MENU____
        file_menu = self.menu_bar.addMenu("&File")
        import_action = file_menu.addAction("Import")
        export_action = file_menu.addMenu("Export")
        export_json_action = export_action.addAction("Export")
        export_text_action = export_action.addAction("Export (.txt)")
        template_action = file_menu.addAction("Template")
        save_action = file_menu.addAction("Save")

        #___PREFERENCE MENU___
        preference_menu = self.menu_bar.addMenu("&Preference")
        mode_action = preference_menu.addMenu("Modes")
        light_mode_action = mode_action.addAction("Light Mode")
        dark_mode_action = mode_action.addAction("Dark Mode")
        auto_mode_action = mode_action.addAction("Auto Mode")
        font_action = preference_menu.addAction("Change Font")
        self.sound_action = preference_menu.addAction("Toggle Sound")
        self.sound_action.setCheckable(True)
        self.sound_action.setChecked(True)

        #___MODIFY MENU___
        modify_menu = self.menu_bar.addMenu("&Modify")
        compare_action = modify_menu.addAction("Compare Lists")
        merge_action = modify_menu.addAction("Merge Lists")
        identification_action = modify_menu.addAction("Auto Identification")

        #___SEARCH MENU___
        search_action = self.menu_bar.addAction("&Search")


        # Connect menu actions to methods
        #___FILE ACTIONS___
        import_action.triggered.connect(self.import_requirements)
        export_json_action.triggered.connect(self.export_requirements)
        export_text_action.triggered.connect(self.export_requirements_as_txt)
        template_action.triggered.connect(self.requirement_template)
        save_action.triggered.connect(self.save_progress)

        #___PREFERENCE ACTIONS___
        light_mode_action.triggered.connect(self.light_mode)
        dark_mode_action.triggered.connect(self.dark_mode)
        auto_mode_action.triggered.connect(self.auto_mode)
        font_action.triggered.connect(self.change_font)
        self.sound_action.triggered.connect(self.toggle_sound)

        #___MODIFY ACTIONS___
        compare_action.triggered.connect(self.compare_requirements)
        merge_action.triggered.connect(self.merge_requirements)
        identification_action.triggered.connect(self.automatic_identification)

        #___SEARCH ACTIONS___
        search_action.triggered.connect(self.search)

    # Method for dark mode
    def dark_mode(self):
        qdarktheme.setup_theme("dark")

    # Method for light mode
    def light_mode(self):
        qdarktheme.setup_theme("light")

    # Method to follow device's mode
    def auto_mode(self):
        qdarktheme.setup_theme("auto")

    # Method for changing app font      
    def change_font(self):
        ok, font = QFontDialog.getFont(self.window)
        if ok:
            self.window.app.setFont(font) 

            # Recursively apply to existing widgets
            def apply_font_recursively(widget):
                widget.setFont(font)
                for child in widget.findChildren(QWidget):
                    apply_font_recursively(child)

            apply_font_recursively(self.window)

    # Method for turning sound on/off
    def toggle_sound(self):
        is_checked = self.sound_action.isChecked()
        self.media_player.toggle_sound(is_checked)

    # Method for importing requirement list (.json)
    def import_requirements(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Import Requirements", "", "JSON Files (*.json)")

        if filepath:
            try:
                data = FileOperations.read_file(filepath)
                title, author, requirements = FileOperations.dictionary_to_table(data)

                tab = RequirementSection(self.warning_widget,self.conflict_detector,title=title, author=author)
                tab.table.setRowCount(len(requirements))
                for row, item in enumerate(requirements):
                    tab.table.setItem(row, 0, QTableWidgetItem(str(item.get("requirementID", ""))))
                    tab.table.setItem(row, 1, QTableWidgetItem(str(item.get("requirement", ""))))
                    tab.table.setItem(row, 2, QTableWidgetItem(str(item.get("attributes", ""))))

                self.tab_widget.insertTab(self.tab_widget.count() - 1, tab, title)
                self.tab_widget.setCurrentWidget(tab)

                QMessageBox.information(self, "Import Successful", f"Imported {len(requirements)} requirements.")

            except Exception as e:
                QMessageBox.critical(self, "Import Failed", f"Error: {e}")   

    # Method for exporting requirement list (.json)
    def export_requirements(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Requirements", "", "JSON Files (*.json)")

        if filepath:
            widget = self.tab_widget.currentWidget()
            if isinstance(widget, RequirementSection):
                data = FileOperations.table_to_dictionary(widget.get_title(), widget.get_author(), widget.get_table_contents())
                FileOperations.write_file(filepath, data)
                QMessageBox.information(self, "Export Successful", f"Exported to {filepath}")
            else:
                QMessageBox.warning(self, "Export Error", "Not a requirement tab!")

    # Method for exporting requirement list (.txt)           
    def export_requirements_as_txt(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save Requirements as TXT", "", "Text Files (*.txt)")

        if filepath:
            widget = self.tab_widget.currentWidget()
            if isinstance(widget, RequirementSection):
                title = widget.get_title()
                author = widget.get_author()
                table_data = widget.get_table_contents()

                lines = []
                lines.append(f"Title: {title}")
                lines.append(f"Author: {author}")
                lines.append("\nRequirements:")
                lines.append("Row | ID | Description | Attributes")
                lines.append("-" * 60)

                for row, req_id, req_text, req_att in table_data:
                    lines.append(f"{row} | {req_id} | {req_text} | {req_att}")

                try:
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write("\n".join(lines))
                    QMessageBox.information(self, "Export Successful", f"Exported to {filepath}")
                except Exception as e:
                    QMessageBox.critical(self, "Export Failed", f"An error occurred:\n{str(e)}")
            else:
                QMessageBox.warning(self, "Export Error", "Not a requirement tab!")

    # Method for getting requirement templates
    def requirement_template(self):
        # Available templates mapped to their variable names
        templates = {
            "Regular Template": "regular_template",
            "Functional Web App Template": "func_web_template",
            "Non-functional Web App Template": "nonfunc_web_template"
        }

        # Ask user to select one
        options = list(templates.keys())
        selected_label, ok = QInputDialog.getItem(self, "Choose Template", "Select a requirement template:", options, 0, False)

        if not ok or not selected_label:
            return  # Cancelled          
              
        try:
            data =  getattr(template, templates[selected_label])
            title, author, requirements = FileOperations.dictionary_to_table(data)

            tab = RequirementSection(self.warning_widget,self.conflict_detector,title=title, author=author)
            tab.table.setRowCount(len(requirements))
            for row, item in enumerate(requirements):
                tab.table.setItem(row, 0, QTableWidgetItem(item.get("requirementID", "")))
                tab.table.setItem(row, 1, QTableWidgetItem(item.get("requirement", "")))

            # MAY HAVE SIMILAR ISSUE IN TABSECTION, ADD TAB
            self.tab_widget.insertTab(self.tab_widget.count() - 1, tab, title)
            self.tab_widget.setCurrentWidget(tab)

            QMessageBox.information(self, "Import Template Successful", f"Imported {len(requirements)} requirements.")

        except Exception as e:
            QMessageBox.critical(self, "Import Template Failed", f"Error: {e}")   

    # Method for comparing between requirement list
    def compare_requirements(self):
        # Ask user which tab to compare with
        current_index = self.tab_widget.currentIndex()
        plus_tab_index = self.tab_widget.count() - 1
        
        # Remove current tab from the list can't compare with itself)(
        compare_options = [
            self.tab_widget.tabText(i)
            for i in range(self.tab_widget.count())
            if i != current_index and i != plus_tab_index
        ]
        compare_indices = [
            i
            for i in range(self.tab_widget.count())
            if i != current_index and i != plus_tab_index
        ]

        if not compare_options:
            QMessageBox.warning(self, "No Tabs Available", "There are no other tabs to compare with.")
            return

        selected_tab_name, ok = QInputDialog.getItem(
            self,
            "Compare Requirements",
            "Select a tab to compare with:",
            compare_options,
            editable=False
        )

        if not ok:
            return

        selected_index = compare_indices[compare_options.index(selected_tab_name)]

        # Step 2: Identify Tab A and Tab B
        tab_A = self.tab_widget.widget(current_index)
        tab_B = self.tab_widget.widget(selected_index)

        # Step 3: Get combined content
        contents_A = tab_A.get_table_contents()
        contents_B = tab_B.get_table_contents()
        combined_contents = contents_A + contents_B  # Or do a smarter merge if needed

        # Step 4: Run conflict detection
        conflicts = self.conflict_detector.detect_conflict(combined_contents)

        # Step 5: Highlight conflicts in both tables
        tab_A.show_combined_conflicts(conflicts)
        tab_B.show_combined_conflicts(conflicts)

    # Method for merging between requirement list
    def merge_requirements(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Import Requirements", "", "JSON Files (*.json)")

        if filepath:
            try:
                # Read and parse file
                data = FileOperations.read_file(filepath)
                title, author, requirements = FileOperations.dictionary_to_table(data)

                tab = self.tab_widget.currentWidget()

                if isinstance(tab, RequirementSection):
                    table = tab.table
                    current_rows = table.rowCount()
                    new_rows = len(requirements)
                    table.setRowCount(current_rows + new_rows)

                    # Append new requirements
                    for i, item in enumerate(requirements):
                        row = current_rows + i
                        table.setItem(row, 0, QTableWidgetItem(str(item.get("requirementID", ""))))
                        table.setItem(row, 1, QTableWidgetItem(str(item.get("requirement", ""))))
                        table.setItem(row, 2, QTableWidgetItem(str(item.get("attributes", ""))))

                    QMessageBox.information(self, "Merge Successful", f"Merged {new_rows} requirements into current tab.")

            except Exception as e:
                QMessageBox.critical(self, "Merge Failed Failed", f"Error: {e}") 

    # Method for automatically create requirement ID (eg. REQ-001)
    def automatic_identification(self):
        current_tab = self.tab_widget.currentWidget()
        dialog = QDialog(self)
        dialog.setWindowTitle("Auto ID Generator")
        layout = QFormLayout(dialog)
       
        start_row = QSpinBox()
        start_row.setMinimum(1)

        end_row = QSpinBox()
        end_row.setMinimum(1)

        prefix = QLineEdit("REQ")
        infix = QLineEdit("0001")
        suffix = QLineEdit("")

        layout.addRow("Start Row:", start_row)
        layout.addRow("End Row:", end_row)
        layout.addRow("Prefix:", prefix)
        layout.addRow("Infix Format (e.g., 0001):", infix)
        layout.addRow("Suffix:", suffix)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)

        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        if dialog.exec() != QDialog.Accepted:
            return

        try:
            start_num = int(infix.text())
            num_digits = len(infix.text())
        except ValueError:
            QMessageBox.warning(self, "Invalid Infix", "Infix must be numeric like '001' or '0007'.")
            return

        table = current_tab.table
        max_row = table.rowCount()

        if end_row.value() > max_row or start_row.value() > end_row.value():
            QMessageBox.warning(self, "Invalid Row Range", f"Row range must be between 1 and {max_row}.")
            return

        # Generate and assign IDs
        for row in range(start_row.value()-1, end_row.value()):
            new_id = f"{prefix.text()}{str(start_num).zfill(num_digits)}{suffix.text()}"
            table.setItem(row, 0, QTableWidgetItem(new_id))
            start_num += 1

    # Method for saving progress in app
    def save_progress(self):
        self.backup.perform_backup()

    # Method for searching item in requirement list
    def search(self):
        # Ask the user for search text
        current_tab = self.tab_widget.currentWidget()

        text, ok = QInputDialog.getText(self, "Search Table", "Enter text to search:")

        if ok and text:
            current_tab.clear_highlights()
            matches = current_tab.search_table(text)

            if matches:
                table = current_tab.table  
                for row, col in matches:
                    item = table.item(row, col)
                    item.setSelected(True)
                    table.scrollToItem(item)
                    current_tab.highlight_rows([row], "darkBlue")
            else:
                QMessageBox.information(self, "Search Result", "No matches found.")





