from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy
from PySide6.QtCore import Qt, Signal, QObject

class WarningSection(QWidget):
    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # # Temporary button
        # trigger_button = QPushButton("Trigger Warning")
        # main_layout.addWidget(trigger_button)

        # Scroll area for warning messages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_frame = QWidget()
        self.warning_layout = QVBoxLayout()
        scroll_frame.setLayout(self.warning_layout)
        scroll.setWidget(scroll_frame)
        main_layout.addWidget(scroll)

        # # Connect button to add dummy warning
        # trigger_button.clicked.connect(self.add_dummy_warning)

    # def add_dummy_warning(self):
    #     self.add_warning("Warning: Requirement Conflict Found!")
    #     self.conflict_warning(
    #         {
    #         "redundancy" : [[0,1]],
    #         "similarity": [[2,3]],
    #         "contradiction": [[4,5]]
    #     }
    #     )


    def clear_warnings(self):
        while self.warning_layout.count():
            child = self.warning_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


    def add_warning(self, text, type=None):
        bubble = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # remove outer padding
        layout.setSpacing(0)
        bubble.setLayout(layout)
        
        label = QLabel(text)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum) 

        if type == 1:
            label.setStyleSheet("""
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 8pt;
            """)
            
        else:
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

        conflict_type = ["similarity", "redundancy", "contradiction"]
        total = sum(len(conflicts.get(key, [])) for key in conflict_type)

        if total > 0:
            self.add_warning(f"{total} conflicts found!", 1)

            for x in conflict_type:
                for (row1, id1), (row2, id2) in conflicts.get(x, []):
                    label1 = id1 if id1 else f"Row {row1 + 1}"
                    label2 = id2 if id2 else f"Row {row2 + 1}"
                    if x == "similarity":
                        self.add_warning(f"🟡 Similarity: {label1} and {label2}")
                    if x == "redundancy":
                        self.add_warning(f"🔴 Redundancy: {label1} and {label2}")
                    if x == "contradiction":
                        self.add_warning(f"🟠 Contradiction: {label1} and {label2}")
        else:
            self.add_warning("🟢 No conflict detected.")

    # def solve_conflict(self, conflict={}):
