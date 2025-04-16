from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QGridLayout, QLabel,
    QTableWidget,QTableWidgetItem, QPushButton, QVBoxLayout, QHBoxLayout)

class MainWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Requirements Conflict Detection Software")

        # Layout
        central_widget = QWidget()
        layout = QGridLayout()

        # MenuBar and Menus
        menu_bar = self.menuBar()

        settings_menu = menu_bar.addMenu("&Settings")
        compare_action = settings_menu.addAction("Compare Lists")
        merge_action = settings_menu.addAction("Merge Lists")
        template_action = settings_menu.addAction("Template")
        import_action = settings_menu.addAction("Import")
        export_action = settings_menu.addAction("Export")

        # Labels (Temporary)
        # --- HEADER (will be tabs later) ---
        header_label = QLabel("Tabs go here later")
        header_label.setStyleSheet("background-color: gray;")
        header_label.setFixedHeight(50)  # thin header
        layout.addWidget(header_label, 0, 0, 1, 2)  # row 0, col 0→1

        # --- CENTER TABLE AREA ---
        # table_label = QLabel("Table goes here")
        # table_label.setStyleSheet("background-color: blue;")
        # layout.addWidget(table_label, 1, 0)

        # Table
        table = QTableWidget(5, 2)
        table.setHorizontalHeaderLabels(["Requirement", "Details"])

        # Optional: fill with dummy data
        table.setItem(0, 0, QTableWidgetItem("REQ-001"))
        table.setItem(0, 1, QTableWidgetItem("User can log in"))

        # Make it writable: QTableWidget is writable by default!
        layout.addWidget(table, 1, 0)

        # --- WARNING AREA (right side) ---
        warning_label = QLabel("Warnings go here")
        warning_label.setStyleSheet("background-color: darkmagenta;")
        layout.addWidget(warning_label, 1, 1)

        # Set column stretches: left wider than right
        layout.setColumnStretch(0, 3)  # main content area
        layout.setColumnStretch(1, 1)  # warning area

        # Set Layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        # # Tabs
        # tab_widget = QTabWidget(self)
        # widget_list_1 = QWidget()
        # widget_list_2 = QWidget()
        # tab_widget.addTab(widget_list_1,"List 1")
        # # tab_widget.addTab(widget_list_1,"List 2")

        # # layout = QVBoxLayout()
        # grid_layout.addWidget(tab_widget,0,1)

        # self.setLayout(grid_layout)