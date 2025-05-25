
from modules.spacyImplementation import SpacyImplementation

class ConflictSolver:
    def __init__(self):
        self.spacy = SpacyImplementation()

    # Note, item is a pair of conflict
    # item = ((row,id,requirement),(row,id,requirement))
    # item1 = (row,id,requirement)

    def solve_conflict(self, conflict_type="", item1=None, item2=None, choice=None):
        if conflict_type == "redundancy":
            return self.solve_redundancy(item1, item2, choice)
        elif conflict_type == "similarity":
            return self.solve_similarity(item1, item2, choice)
        elif conflict_type == "contradiction":
            return self.solve_contradiction(item1, item2, choice)
        else:
            return None

    def resolve_by_choice(self, item1=None, item2=None, choice=None):
        if choice == item1:
            return item1
        elif choice == item2:
            return item2
        else:
            return None

    def solve_redundancy(self, item1=None, item2=None, choice=None):
        return self.resolve_by_choice(item1, item2, choice)

    def solve_similarity(self, item1=None, item2=None, choice=None):
        return self.resolve_by_choice(item1, item2, choice)

    def solve_contradiction(self, item1=None, item2=None, choice=None):
        return self.resolve_by_choice(item1, item2, choice)
    
    def solve_ambiguity(self, sentence):
        return self.spacy.replace_vague_with_strong(sentence)
    
    def seperate_items(self,conflict_pair=(),item_num=None):
        item1, item2 = conflict_pair

        if item_num == 1:
            return item1
        elif item_num == 2:
            return item2
        else:
            return None 
