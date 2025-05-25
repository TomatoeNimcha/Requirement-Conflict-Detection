from PySide6.QtGui import QColor, QBrush

from modules.spacyImplementation import SpacyImplementation


class ConflictDetector:
    def __init__(self):
        self.spacy = SpacyImplementation()
        self.spacy.is_spacy_running()

    def detect_conflict(self,table_contents=[]):
        conflicts_redundancy = []
        conflicts_similarity = []
        conflicts_contradiction = []
        conflicts_ambiguity = []

        # STEP 1: Preprocess and cache Spacy Docs
        docs = []
        for _, _, req, _ in table_contents:
            if not req.strip():
                docs.append(None)
            else:
                docs.append(self.spacy.get_nlp(req))

        for i in range(len(table_contents)):
            row, id_, req, _ = table_contents[i]
            if self.spacy.ambiguity_check(req):
                conflicts_ambiguity.append((row, id_, req))

        # STEP 2: Compare only valid pairs
        for i in range(len(table_contents)):
            row1, id1, req1, _ = table_contents[i]
            doc1 = docs[i]
            if doc1 is None:
                continue

            for j in range(i + 1, len(table_contents)):
                row2, id2, req2, _ = table_contents[j]
                doc2 = docs[j]
                if doc2 is None:
                    continue

                similarity = self.spacy.spacy_similarity(doc1, doc2)
                pair = ((row1, id1, req1), (row2, id2, req2))

                if self.spacy.redundancy_check(similarity):
                    conflicts_redundancy.append(pair)
                if self.spacy.similarity_check(similarity):    
                    if self.spacy.contradiction_check(similarity, req1, req2):
                        conflicts_contradiction.append(pair)
                    else:
                        conflicts_similarity.append(pair)

        return {
            "redundancy": conflicts_redundancy,
            "similarity": conflicts_similarity,
            "contradiction": conflicts_contradiction,
            "ambiguity" : conflicts_ambiguity
        }
    
    def total_confict(self, detect_conflict_result={}):
        total = len(detect_conflict_result.get("redundancy", [])) 
        total += len(detect_conflict_result.get("similarity", [])) 
        total += len(detect_conflict_result.get("contradiction", [])) 
        total += len(detect_conflict_result.get("ambiguity", [])) 
        return total
        
    def extract_rows(self, conflict_list, num):
        if num == 2 :
            return [(a[0], b[0]) for a, b in conflict_list]
        else:
            return [a[0] for a in conflict_list]
        
    def extract_ids(self, conflict_list, num):
        if num == 2 :
            return [(a[1], b[1]) for a, b in conflict_list]
        else:
            return [a[1] for a in conflict_list]

    def extract_reqs(self, conflict_list, num):
        if num == 2 :
            return [(a[2], b[2]) for a, b in conflict_list]
        else:
            return [a[2] for a in conflict_list]
    
    def progress(self, current, total):
        return int((current / total) * 100)

    
    

