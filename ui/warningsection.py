from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt, Signal, QObject

from modules.conflictSolver import ConflictSolver

class WarningSection(QWidget):
    def __init__(self, tab_widget):
        super().__init__()

        self.conflict_solver = ConflictSolver()
        self.tab_widget = tab_widget

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Scroll area for warning messages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)


        #Scroll_frame
        scroll_frame = QWidget()
        scroll.setWidget(scroll_frame)


        self.warning_layout = QVBoxLayout()
        self.warning_layout.setAlignment(Qt.AlignTop)
        scroll_frame.setLayout(self.warning_layout)
        scroll_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        main_layout.addWidget(scroll)

    def set_tab_widget(self,tab_widget):
        self.tab_widget = tab_widget


    def clear_warnings(self):
        while self.warning_layout.count():
            child = self.warning_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def delete_warning(self, warning):
        if warning is not None:
            warning.warning_layout.removeWidget(warning)
            warning.setParent(None)
            warning.deleteLater()



    def add_warning(self, warning_type, text1="Top", text2="Desc", conflict_type=None, item1=None, item2=None):
        bubble = QWidget()
        bubble.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        
        layout = QVBoxLayout()
        # layout.setContentsMargins(8, 8, 8, 8)  # Inner padding inside the border
        layout.setSpacing(6)
        bubble.setLayout(layout)

        # Add a border to the entire bubble
        bubble.setStyleSheet("""
            QWidget {
                border: 0.5px solid gray;
                border-radius: 6px;
            }
        """)

        # Title
        title_label = QLabel(f"{warning_type} : {text1} !")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        title_label.setStyleSheet("""
            border: None;
            font-weight: bold;
            font-size: 9pt;
        """)
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(text2)
        desc_label.setWordWrap(True)
        desc_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        desc_label.setStyleSheet("""
            font-size: 8pt;
        """)
        layout.addWidget(desc_label)

        # Quick Fix Button
        quick_fix_btn = QPushButton("Quick Fix")
        quick_fix_btn.setStyleSheet("""
            padding: 4px 10px;
            font-size: 8pt;
        """)
        layout.addWidget(quick_fix_btn, alignment=Qt.AlignRight)

        # Add the bubble to the warning layout
        self.warning_layout.setAlignment(Qt.AlignTop)
        self.warning_layout.addWidget(bubble)
        quick_fix_btn.clicked.connect(lambda: self.solve_warning(conflict_type, item1, item2))

    def add_status(self, text):
        bubble = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # remove outer padding
        layout.setSpacing(0)
        bubble.setLayout(layout)
        
        label = QLabel(text)
        label.setWordWrap(True)
        label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum) 
        label.setStyleSheet("""
            padding: 4px 8px;
            font-size: 8pt;
        """)
            
        layout.addWidget(label)
        self.warning_layout.setAlignment(Qt.AlignTop)
        self.warning_layout.addWidget(bubble)

    def conflict_warning(self,conflicts={},table=None):
        self.clear_warnings()
        print("This is conflict warning")
        print(conflicts)

        conflict_type = ["similarity", "redundancy", "contradiction"]
        total = sum(len(conflicts.get(key, [])) for key in conflict_type)

        if total > 0:
            self.add_status(f"{total} conflict(s) found!")

            for conflict_type in conflict_type:
                for conflict_pair in conflicts.get(conflict_type, []):
                    item1, item2 = conflict_pair
                    row1, id1, req1 = item1
                    row2, id2, req2 = item2

                    label1 = id1 if id1 else f"Row {row1 + 1}"
                    label2 = id2 if id2 else f"Row {row2 + 1}"

                    if conflict_type == "redundancy":
                        self.add_warning("🔴 Redundancy", f"{label1} and {label2}", f"{label1} and {label2} are the same requirement!\nRemove one of them.", conflict_type, item1, item2)
                    elif conflict_type == "similarity":
                        self.add_warning("🟡 Similarity", f"{label1} and {label2}", f"{label1} and {label2} are too similar!", conflict_type, item1, item2)
                    elif conflict_type == "contradiction":
                        self.add_warning("🟠 Contradiction", f"{label1} and {label2}", f"{label1} and {label2} contradict each other!", conflict_type, item1, item2)
        else:
            self.add_status("🟢 No conflict detected.")

    def solve_warning(self, warning_type, item1, item2):
        row1, id1, req1 = item1
        row2, id2, req2 = item2

        print(f"Fixing {warning_type.lower()} conflict between Row {row1 + 1} and Row {row2 + 1}")

        # Ask the user which one to keep
        msg = QMessageBox()
        msg.setWindowTitle("Resolve Conflict")
        msg.setText(
            f"Which requirement do you want to keep?\n\n"
            f"Option A (Row {row1 + 1}):\n{id1 or '(No ID)'}\n{req1}\n\n"
            f"Option B (Row {row2 + 1}):\n{id2 or '(No ID)'}\n{req2}"
        )
        msg.setIcon(QMessageBox.Question)

        btn_a = msg.addButton(f"Keep Row {row1 + 1}", QMessageBox.AcceptRole)
        btn_b = msg.addButton(f"Keep Row {row2 + 1}", QMessageBox.RejectRole)
        msg.addButton(QMessageBox.Cancel)

        msg.exec_()

        if msg.clickedButton() == btn_a:
            choice = item1
            to_remove = item2
        elif msg.clickedButton() == btn_b:
            choice = item2
            to_remove = item1
        else:
            return

        # Resolve conflict
        result = self.conflict_solver.solve_conflict(warning_type, item1, item2, choice)
        print("Result:", result)

        if result is not None:
            kept_row, kept_id, kept_req = result
            self.add_status(f"✅ Conflict resolved. Kept: {kept_id or f'Row {kept_row + 1}'}")

            # ✅ Remove the row that was NOT chosen
            if self.tab_widget:
                current_section = self.tab_widget.currentWidget()
                if hasattr(current_section, "remove_conflict_row"):
                    current_section.remove_conflict_row(to_remove[0])
                    current_section.show_conflicts()
        else:
            self.add_status("⚠️ Could not resolve conflict.")


