from PySide6.QtGui import QColor, QBrush

from modules.spacyImplementation import SpacyImplementation


class ConflictDetector:
    def __init__(self):
        self.spacy = SpacyImplementation()
        self.spacy.is_spacy_running()

    def detect_conflict(self,table_contents=[]):
    # Note that anything that needs spacy is directly implemented in spacyImplementation
    # Not a nerd but its so only need to call the large package and english nlp once
        conflicts_redundancy = []
        conflicts_similarity = []
        conflicts_contradiction = []

        # Compare pairs
        for i in range(len(table_contents)):
            row1, id1, text1, attribute1 = table_contents[i]
            for j in range(i + 1, len(table_contents)):
                row2, id2, text2, attribute2 = table_contents[j]

                similarity = self.spacy.spacy_similarity(text1, text2)
                pair = ((row1, id1), (row2, id2))

                if self.spacy.redundancy_check(similarity):
                    conflicts_redundancy.append(pair)
                if self.spacy.similarity_check(similarity):    
                    if self.spacy.contradiction_check(similarity, text1, text2):
                        conflicts_contradiction.append(pair)
                    else:
                        conflicts_similarity.append(pair)

        #conflict list with row and id
        return {
            "redundancy": conflicts_redundancy,
            "similarity": conflicts_similarity,
            "contradiction": conflicts_contradiction
        }
    
    def total_confict(self, detect_conflict_result={}):
        total = len(detect_conflict_result.get("redundancy", [])) + len(detect_conflict_result.get("similarity", [])) + len(detect_conflict_result.get("contradiction", []))
        return total
    
    def extract_rows(self, conflict_list):
        return [(a[0], b[0]) for a, b in conflict_list]
        
    def extract_ids(self, conflict_list):
        return [(a[1], b[1]) for a, b in conflict_list]

    
    

