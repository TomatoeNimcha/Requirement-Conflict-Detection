import sys
from PySide6.QtWidgets import QApplication
from ui.mainwindow import MainWindow

app = QApplication(sys.argv)
window = MainWindow(app)
# Resize window
window.resize(800, 500)
window.show()
app.exec()


#this is spacy
# import spacy

# # Create a blank English nlp object
# nlp = spacy.blank("en")

# # Created by processing a string of text with the nlp object
# doc = nlp("Hello world!")

# # Iterate over tokens in a Doc
# for token in doc:
#     print(token.text)