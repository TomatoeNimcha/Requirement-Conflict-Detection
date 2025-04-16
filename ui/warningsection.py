from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PySide6.QtCore import Qt

class WarningSection(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Temporary button
        trigger_button = QPushButton("Trigger Warning")
        main_layout.addWidget(trigger_button)

        # Scroll area for warning messages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_frame = QWidget()
        self.warning_layout = QVBoxLayout()
        scroll_frame.setLayout(self.warning_layout)
        scroll.setWidget(scroll_frame)
        main_layout.addWidget(scroll)

        # Connect button to add dummy warning
        trigger_button.clicked.connect(self.add_dummy_warning)

    def add_dummy_warning(self):
        self.add_warning("Warning: Requirement Conflict Found!")

    def add_warning(self, text):
        warning_label = QLabel(text)
        warning_label.setWordWrap(True)
        warning_label.setStyleSheet("""
            background-color: red;
            padding: 6px;
            border-radius: 8px;
        """)
        warning_label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.warning_layout.addWidget(warning_label, alignment=Qt.AlignTop)