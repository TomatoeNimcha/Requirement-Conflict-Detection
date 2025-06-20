from PySide6.QtWidgets import QWidget, QTabWidget, QWidget, QInputDialog, QTabBar, QMessageBox

from ui.requirementsection import RequirementSection

# Class for tabs below the menu bar
class TabSection(QTabWidget):
    def __init__(self, warning_widget, conflict_detector):
        super().__init__()

        # Variables
        self.warning_widget = warning_widget
        self.conflict_detector = conflict_detector

        # Set tab style and closability
        self.setStyleSheet("QTabBar::tab { height: 30px; padding: 8px; }")
        self.setTabsClosable(True)

        # # Add initial tabs
        # if self.backup_check == True:
        #     self.add_requirement_tab(title="Requirement List")

        # Add "+" tab
        self.plus_tab = QWidget()
        self.addTab(self.plus_tab, "+")
        plus_index = self.indexOf(self.plus_tab)
        self.tabBar().setTabButton(plus_index, QTabBar.RightSide, None)

        # Watch for tab changes
        self.currentChanged.connect(self.user_add_requirement_tab)
        self.tabCloseRequested.connect(self.close_tab)

    # Method for when user adds requirement tab
    def user_add_requirement_tab(self, index):
        if self.tabText(index) == "+":
            # 1. Ask for tab name
            name, ok = QInputDialog.getText(self, "New Tab", "Enter name for this requirement list:")

            if not ok or not name.strip():
                self.setCurrentIndex(0)            
            else:
                self.add_requirement_tab(title=name)

    # Method for when system adds requirement tab
    def add_requirement_tab(self, title=None, author=None):
        index = self.count() - 1  # always insert before "+" tab
        tab_name = title if title else f"List {index + 1}"
        tab = RequirementSection(self.warning_widget,self.conflict_detector,title=tab_name)
        self.insertTab(index, tab, tab_name)
        self.setCurrentIndex(index)  
 
        return tab

    # Method for closing tab
    def close_tab(self, index):
        # Prevent closing the "+" tab
        if self.widget(index) == self.plus_tab:
            return
        self.removeTab(index)

        if self.count() == 1 and self.widget(0) == self.plus_tab:
            # Show confirmation dialog
            confirm = QMessageBox.question(
                self,
                "Exit Application?",
                "Do you want to exit the application?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                self.window().close()
            else :
                self.add_requirement_tab(title="Requirement List")



