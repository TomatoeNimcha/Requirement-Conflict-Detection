import sys
from PySide6.QtWidgets import QApplication
from ui.mainwindow import MainWindow
import qdarktheme

# Create the app
app = QApplication(sys.argv)
# Create the window
window = MainWindow(app)
# Automatically style it with qdarktheme
qdarktheme.setup_theme("auto")

# Resize window
window.resize(800, 500)
window.show()

# Execute app
app.exec()
