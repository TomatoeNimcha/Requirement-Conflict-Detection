from PySide6.QtGui import QColor, QBrush

from modules.spacyImplementation import SpacyImplementation


class ConflictDetector:
    def __init__(self):
        self.spacy = SpacyImplementation()


    def detect_conflict(self,table_contents=[]):
    # Note that anything that needs spacy is directly implemented in spacyImplementation
    # Not a nerd but its so only need to call the large package and english nlp once
        conflicts_redundancy = []
        conflicts_similarity = []
        conflicts_contradiction = []

        # Compare pairs
        for i in range(len(table_contents)):
            row1, id1, text1 = table_contents[i]
            for j in range(i + 1, len(table_contents)):
                row2, id2, text2 = table_contents[j]
                similarity = self.spacy.spacy_similarity(text1, text2)

                if self.spacy.redundancy_check(similarity):
                    conflicts_redundancy.append((row1, row2))
                if self.spacy.similarity_check(similarity):
                    conflicts_similarity.append((row1, row2))
                if self.spacy.contradiction_check(similarity, text1, text2):
                    conflicts_contradiction.append((row1, row2))

        return {
            "redundancy": conflicts_redundancy,
            "similarity": conflicts_similarity,
            "contradiction": conflicts_contradiction
        }
