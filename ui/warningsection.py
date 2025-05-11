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
        self.conflict_warning(
            {
            "redundancy" : [[0,1]],
            "similarity": [[2,3]],
            "contradiction": [[4,5]]
        }
        )


    def clear_warnings(self):
        while self.warning_layout.count():
            child = self.warning_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def add_warning(self, text):
        bubble = QWidget()
        layout = QVBoxLayout()
        bubble.setLayout(layout)
        
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet("""
            background-color: #ffe6e6;
            border: 1px solid #ff4d4d;
            padding: 8px;
            border-radius: 10px;
            color: #990000;
            font-weight: bold;
        """)
        
        layout.addWidget(label)
        self.warning_layout.addWidget(bubble)

    def conflict_warning(self,conflicts={}):
        self.clear_warnings()
        for pair in conflicts["redundancy"]:
            self.add_warning(f"Redundancy: Row {pair[0]} and {pair[1]}")
        for pair in conflicts["similarity"]:
            self.add_warning(f"Similarity: Row {pair[0]} and {pair[1]}")
        for pair in conflicts["contradiction"]:
            self.add_warning(f"Contradiction: Row {pair[0]} and {pair[1]}")