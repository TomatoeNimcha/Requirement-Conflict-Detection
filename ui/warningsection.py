from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt

from modules.conflictSolver import ConflictSolver

# Class for warning notifications about requirement conflicts
class WarningSection(QWidget):
    def __init__(self, tab_widget, media_player):
        super().__init__()

        # Variables
        self.conflict_solver = ConflictSolver()
        self.tab_widget = tab_widget
        self.media_player = media_player

        # Layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Scroll area for warning messages
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)

        #Scroll_frame
        scroll_frame = QWidget()
        scroll.setWidget(scroll_frame)

        # Warning notification area layout
        self.warning_layout = QVBoxLayout()
        self.warning_layout.setAlignment(Qt.AlignTop)
        scroll_frame.setLayout(self.warning_layout)
        scroll_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        main_layout.addWidget(scroll)

        # Dismiss button below notification area
        dismiss_button = QPushButton("Dismiss Warnings")
        dismiss_button.clicked.connect(self.clear_warnings_and_highlights)
        main_layout.addWidget(dismiss_button)

    # setter for tab widget
    def set_tab_widget(self,tab_widget):
        self.tab_widget = tab_widget

    # Method to clear all warning notifications
    def clear_warnings(self):
        while self.warning_layout.count():
            child = self.warning_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # Method to delete a warning notification
    def delete_warning(self, warning):
        if warning is not None:
            warning.warning_layout.removeWidget(warning)
            warning.setParent(None)
            warning.deleteLater()

    # Method to add warning notification
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

    # Method to clear all warning notification and highlighted list contents
    def clear_warnings_and_highlights(self):
        self.clear_warnings()
        self.tab_widget.currentWidget().clear_highlights()

    # Method to add status into the notification area
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

    # Method to add conflict warning notifications
    def conflict_warning(self, conflicts={}, table=None):
        self.clear_warnings()

        conflict_types = ["similarity", "redundancy", "contradiction"]
        total = sum(len(conflicts.get(key, [])) for key in ["similarity", "redundancy", "contradiction", "ambiguity", "incomplete"])
        total_row = self.tab_widget.currentWidget().get_total_row()  

        if total > 0 or conflicts.get("ambiguity") or conflicts.get("incomplete"):
            self.add_status(f"{total} conflict(s) found between {total_row} rows!" if total else "")

            for conflict_type in conflict_types:
                for conflict_pair in conflicts.get(conflict_type, []):
                    item1, item2 = conflict_pair
                    row1, id1, req1 = item1
                    row2, id2, req2 = item2

                    label1 = id1 if id1 else f"Row {row1 + 1}"
                    label2 = id2 if id2 else f"Row {row2 + 1}"

                    if conflict_type == "redundancy":
                        self.add_warning("🔴 Redundancy", f"{label1} and {label2}",
                                        f"{label1} and {label2} are the same requirement!\nRemove one of them.",
                                        conflict_type, item1, item2)
                    elif conflict_type == "similarity":
                        self.add_warning("🟡 Similarity", f"{label1} and {label2}",
                                        f"{label1} and {label2} are too similar!",
                                        conflict_type, item1, item2)
                    elif conflict_type == "contradiction":
                        self.add_warning("🟠 Contradiction", f"{label1} and {label2}",
                                        f"{label1} and {label2} contradict each other!",
                                        conflict_type, item1, item2)

            for conflict_item in conflicts.get("ambiguity", []):
                row_item, id_item, req_item = conflict_item
                label = id_item if id_item else f"Row {row_item + 1}"
                self.add_warning("🟤 Ambiguity", f"{label}", f"{label} is using ambiguous word(s)!",
                                "ambiguity", conflict_item)
            for conflict_item in conflicts.get("incomplete", []):
                row_item, id_item, req_item = conflict_item
                label = id_item if id_item else f"Row {row_item + 1}"
                self.add_warning("🟥 Incomplete", f"{label}", f"{label} has incomplete written requirement!",
                                "incomplete", conflict_item)
            
            self.media_player.play_warning_sound()
        else:
            self.add_status("🟢 No conflict detected.")

    # Method to solve conflict warning notifications
    def solve_warning(self, warning_type=None, item1=None, item2=None):
        # Single-item conflict
        if item2 is None:
            row_item, id_item, req_item = item1

            msg = QMessageBox()
            
            if warning_type == "ambiguity":
                msg.setWindowTitle("Resolve Ambiguity")
                msg.setText(
                    f"Do you want to automatically fix this ambiguity?\n\n"
                    f"Row {row_item + 1}\n{id_item or '(No ID)'}\n{req_item}"
                )
            elif warning_type == "incomplete":
                msg.setWindowTitle("Remove Incomplete Requirement")
                msg.setText(
                    f"This sentence seems incomplete.\n\n"
                    f"Row {row_item + 1}\n{id_item or '(No ID)'}\n{req_item}\n\n"
                    f"Do you want to delete it?"
                )

            msg.setIcon(QMessageBox.Question)
            btn_accept = msg.addButton("Accept", QMessageBox.AcceptRole)
            msg.addButton(QMessageBox.Cancel)

            msg.exec_()

            if msg.clickedButton() != btn_accept:
                return

            result = self.conflict_solver.solve_conflict(warning_type, item1)

            current_section = self.tab_widget.currentWidget()

            if result is not None:
                if warning_type == "ambiguity":
                    new_text = result
                    self.add_status(f"Ambiguity resolved for {id_item or f'Row {row_item + 1}'}")
                    if hasattr(current_section, "update_row_text"):
                        current_section.update_row_text(row_item, new_text)
                elif warning_type == "incomplete":
                    self.add_status(f"Incomplete requirement deleted: {id_item or f'Row {row_item + 1}'}")
                    if hasattr(current_section, "remove_conflict_row"):
                        current_section.remove_conflict_row(row_item)

                current_section.show_conflicts()
            else:
                self.add_status("Could not resolve conflict.")

        # Pair-item conflict (e.g., redundancy, similarity, contradiction)
        else:
            row1, id1, req1 = item1
            row2, id2, req2 = item2

            msg = QMessageBox()
            msg.setWindowTitle("Resolve Conflict")
            msg.setText(
                f"Which requirement do you want to keep?\n\n"
                f"Option A: \nRow {row1 + 1}\n{id1 or '(No ID)'}\n{req1}\n\n"
                f"Option B: \nRow {row2 + 1}\n{id2 or '(No ID)'}\n{req2}"
            )
            msg.setIcon(QMessageBox.Question)

            btn_a = msg.addButton("Keep A", QMessageBox.AcceptRole)
            btn_b = msg.addButton("Keep B", QMessageBox.RejectRole)
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

            result = self.conflict_solver.solve_conflict(warning_type, item1, item2, choice)

            if result is not None:
                kept_row, kept_id, _ = result
                self.add_status(f"Conflict resolved. Kept: {kept_id or f'Row {kept_row + 1}'}")

                current_section = self.tab_widget.currentWidget()
                if hasattr(current_section, "remove_conflict_row"):
                    current_section.remove_conflict_row(to_remove[0])
                    current_section.show_conflicts()
            else:
                self.add_status("Could not resolve conflict.")




