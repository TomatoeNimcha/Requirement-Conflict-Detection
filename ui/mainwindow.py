from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QGridLayout, QLabel

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
        label_tabs = QLabel("Insert future tabs here")
        label_warning = QLabel("Insert future warnings here")
        label_list = QLabel("Insert future requirement list here")

        # Set Layout
        # layout.addWidget(label_tabs, 0,0,1,3)
        layout.addWidget(label_warning, 1,2,1,1)
        layout.addWidget(label_list, 1,1,1,2)

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