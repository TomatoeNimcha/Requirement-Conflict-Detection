import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QTabWidget, 
    QFileDialog, QPushButton, QVBoxLayout, QWidget
)
from PySide6.QtGui import QAction

def detect_conflicts(texts):
    """Dummy function to process multiple document texts and detect conflicts."""
    conflicts = []
    for i, text in enumerate(texts):
        if "conflict" in text.lower():  # Example rule-based detection
            conflicts.append(f"⚠ Conflict detected in Document {i+1}")

    return "\n".join(conflicts) if conflicts else "✅ No conflicts found."

class MultiTabEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window properties
        self.setWindowTitle("Requirement Conflict Detector")
        self.setGeometry(100, 100, 800, 600)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        # Buttons
        self.new_tab_button = QPushButton("➕ New Tab")
        self.new_tab_button.clicked.connect(self.new_tab)

        self.detect_button = QPushButton("🚀 Detect Conflicts")
        self.detect_button.clicked.connect(self.run_conflict_detection)

        # Layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.addWidget(self.new_tab_button)
        layout.addWidget(self.detect_button)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Menu bar actions
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_action = QAction("New Tab", self)
        new_action.triggered.connect(self.new_tab)
        file_menu.addAction(new_action)

        open_action = QAction("Open File", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction("Save File", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        self.new_tab()  # Start with one tab open

    def new_tab(self, content=""):
        """Creates a new text editor tab."""
        editor = QTextEdit()
        editor.setPlainText(content)
        index = self.tabs.addTab(editor, f"Document {self.tabs.count() + 1}")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        """Closes the selected tab."""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def open_file(self):
        """Opens a file in a new tab."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.new_tab(content)

    def save_file(self):
        """Saves the current tab content to a file."""
        current_widget = self.tabs.currentWidget()
        if current_widget:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)")
            if file_path:
                with open(file_path, "w") as file:
                    file.write(current_widget.toPlainText())

    def run_conflict_detection(self):
        """Runs conflict detection on all open document tabs."""
        texts = [self.tabs.widget(i).toPlainText() for i in range(self.tabs.count())]
        result = detect_conflicts(texts)
        self.new_tab(result)  # Show results in a new tab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiTabEditor()
    window.show()
    sys.exit(app.exec())