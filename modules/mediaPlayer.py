from PySide6.QtCore import  QUrl
from PySide6.QtMultimedia import QSoundEffect

from modules.fileOperations import FileOperations

# Class to play sounds
class MediaPlayer:
    def __init__(self):
        # Variable
        self.sound_enabled = True

        # Warning sound
        self.warning_sound = QSoundEffect()
        source = QUrl.fromLocalFile(FileOperations.get_file_path("media", "pong.wav"))
        self.warning_sound.setSource(source)
        self.warning_sound.setVolume(0.3)

    # Method to toggle sound on/off
    def toggle_sound(self, checked):
        self.sound_enabled = checked

    # Method to play warning sound
    def play_warning_sound(self):
        if self.sound_enabled:
            self.warning_sound.play()

