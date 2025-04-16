import sys
from PySide6.QtWidgets import QApplication
from ui.mainwindow import MainWindow

app = QApplication(sys.argv)
window = MainWindow(app)
# Resize window
window.resize(800, 500)
window.show()
app.exec()
