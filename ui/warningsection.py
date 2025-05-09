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

    # def add_warning(self, text):
    #     warning_label = QLabel(text)
    #     warning_label.setWordWrap(True)
    #     warning_label.setStyleSheet("""
    #         background-color: red;
    #         padding: 6px;
    #         border-radius: 8px;
    #     """)
    #     warning_label.setFrameStyle(QFrame.Panel | QFrame.Raised)
    #     self.warning_layout.addWidget(warning_label, alignment=Qt.AlignTop)

    #     if self.warning_section:
    #         # Clear all previous warnings
    #         for i in reversed(range(self.warning_section.warning_layout.count())):
    #             widget = self.warning_section.warning_layout.itemAt(i).widget()
    #             if widget:
    #                 widget.setParent(None)

    #     if spacy_checker.redundancy_check(text1, text2):
    #         conflicts_redundancy.append((row1, row2))
    #         if self.warning_section:
    #             self.warning_section.add_warning(f"Requirement '{id1}' and '{id2}' are redundant.")

    #     elif spacy_checker.similarity_check(text1, text2):
    #         conflicts_similarity.append((row1, row2))
    #         if self.warning_section:
    #             self.warning_section.add_warning(f"Requirement '{id1}' and '{id2}' are similar.")

    #     elif spacy_checker.contradiction_check(text1, text2):
    #         conflicts_contradiction.append((row1, row2))
    #         if self.warning_section:
    #             self.warning_section.add_warning(f"Requirement '{id1}' and '{id2}' contradict each other.")