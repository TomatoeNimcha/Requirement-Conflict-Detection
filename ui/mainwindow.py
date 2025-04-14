from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QGridLayout

class MainWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Requirements Conflict Detection Software")

        # Layout
        grid_layout = QGridLayout()

        # MenuBar and Menus
        menu_bar = self.menuBar()

        settings_menu = menu_bar.addMenu("&Settings")
        compare_action = settings_menu.addAction("Compare Lists")
        merge_action = settings_menu.addAction("Merge Lists")
        template_action = settings_menu.addAction("Template")
        import_action = settings_menu.addAction("Import")
        export_action = settings_menu.addAction("Export")
        


        # # Tabs
        # tab_widget = QTabWidget(self)
        # widget_list_1 = QWidget()
        # widget_list_2 = QWidget()
        # tab_widget.addTab(widget_list_1,"List 1")
        # # tab_widget.addTab(widget_list_1,"List 2")

        # # layout = QVBoxLayout()
        # grid_layout.addWidget(tab_widget,0,1)

        # self.setLayout(grid_layout)