from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton,QLineEdit
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QColor, QBrush


class TagSection(QWidget):
    def __init__(self, tags=None):
        super().__init__()
        self.tags = tags if tags else []  # List of (name, color) tuples
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.layout.setSpacing(5)

        self.setLayout(self.layout)
        self.render_tags()

    def render_tags(self):
        # Clear old tags
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        # Add new tags
        for tag_text, tag_color in self.tags:
            label = QLabel(tag_text)
            label.setStyleSheet(f"""
                QLabel {{
                    background-color: {tag_color};
                    color: white;
                    border-radius: 10px;
                    padding: 2px 6px;
                    font-size: 10px;
                }}
            """)
            self.layout.addWidget(label)

        self.layout.addStretch()

    def add_tag(self, name, color="#6c757d"):
        if (name, color) not in self.tags:
            self.tags.append((name, color))
            self.render_tags()

    def delete_tag(self, name):
        self.tags = [(n, c) for (n, c) in self.tags if n != name]
        self.render_tags()

    def edit_tag(self, old_name, new_name, new_color=None):
        new_tags = []
        for (name, color) in self.tags:
            if name == old_name:
                new_tags.append((new_name, new_color if new_color else color))
            else:
                new_tags.append((name, color))
        self.tags = new_tags
        self.render_tags()

    def get_tags(self):
        return self.tags
