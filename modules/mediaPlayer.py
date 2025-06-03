from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy, QMessageBox
from PySide6.QtCore import Qt, Signal, QObject, QUrl
from PySide6.QtMultimedia import QSoundEffect

from modules.fileOperations import FileOperations

class MediaPlayer:
    def __init__(self):
        self.sound_enabled = True

        self.warning_sound = QSoundEffect()
        source = QUrl.fromLocalFile(FileOperations.get_file_path("media", "pong.wav"))
        self.warning_sound.setSource(source)
        self.warning_sound.setVolume(0.3)

    def toggle_sound(self, checked):
        self.sound_enabled = checked

    def play_warning_sound(self):
        if self.sound_enabled:
            self.warning_sound.play()

