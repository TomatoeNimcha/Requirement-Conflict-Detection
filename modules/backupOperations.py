

from modules.fileOperations import FileOperations
import os
import json
import datetime

class BackupOperations:
    def __init__(self, tab_widget):
        self.tab_widget = tab_widget
        self.file_operations = FileOperations
        self.BACKUP_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "backup", "backup.json")
        

    def perform_backup(self):
        print("Backup performed")
        all_data = []
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)

            title = widget.get_title()
            author = widget.get_author()
            table = widget.get_table_contents()
            data = FileOperations.table_to_dictionary(title, author, table)
            all_data.append(data)

        with open(self.BACKUP_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)

    def retrieve_backup(self):
        print("Backup Retrieved")
        if self.is_backup_empty() == True:
            return
        if not os.path.exists(self.BACKUP_FILE):
            return

        with open(self.BACKUP_FILE, 'r', encoding='utf-8') as f:
            all_data = json.load(f)

        for data in all_data:
            title, author, requirements = FileOperations.dictionary_to_table(data)

            new_tab = self.tab_widget.add_requirement_tab(title, author)
            
            while new_tab.table.rowCount() > 0:
                new_tab.table.removeRow(0)

            for item in requirements:
                new_tab.add_row()
                row_index = new_tab.table.rowCount() - 1
                new_tab.update_any_text(row_index, 0, str(item.get("requirementID", "")))
                new_tab.update_any_text(row_index, 1, str(item.get("requirement", "")))
                new_tab.update_any_text(row_index, 2, str(item.get("attributes", "")))
            new_tab.add_row()

    def is_backup_empty(self):
        if os.path.getsize(self.BACKUP_FILE) == 0:
            return True
        else:
            return False