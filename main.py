import sys
from PySide6.QtWidgets import QApplication
from ui.mainwindow import MainWindow
import qdarktheme

# qdarktheme.enable_hi_dpi()

app = QApplication(sys.argv)
window = MainWindow(app)
qdarktheme.setup_theme("auto")

# Resize window
window.resize(800, 500)
window.show()
app.exec()
