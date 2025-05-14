from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy
from PySide6.QtCore import Qt, Signal, QObject

class WarningSection(QWidget):
    requirement_conflict_signal = Signal(dict)
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

        self.requirement_conflict_signal.connect(self.conflict_warning)

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
        layout.setContentsMargins(0, 0, 0, 0)  # remove outer padding
        layout.setSpacing(0)
        bubble.setLayout(layout)
        
        label = QLabel(text)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum) 
        label.setStyleSheet("""
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 4px 8px;
            font-size: 8pt;
        """)
        
        layout.addWidget(label)
        self.warning_layout.setAlignment(Qt.AlignTop)
        self.warning_layout.addWidget(bubble)

    def conflict_warning(self,conflicts={}):
        self.clear_warnings()
        print("This is conflict warning")
        print(conflicts)

        if conflicts!={}: #This is done to avoid str warning
            for pair in conflicts["similarity"]:
                self.add_warning(f"🟡 Similarity: Row {pair[0]+1} and {pair[1]+1}")
            for pair in conflicts["redundancy"]:
                self.add_warning(f"🔴 Redundancy: Row {pair[0]+1} and {pair[1]+1}")
            for pair in conflicts["contradiction"]:
                self.add_warning(f"🟠 Contradiction: Row {pair[0]+1} and {pair[1]+1}")

        if conflicts == {"redundancy": [], "similarity": [], "contradiction": []}:
            self.add_warning("🟢 No conflict detected.")