
from modules.spacyImplementation import SpacyImplementation

# Class containing methods to solve conflicts
class ConflictSolver:
    def __init__(self):
        # Variable
        self.spacy = SpacyImplementation()

    # Note, item is a pair of conflict
    # item = ((row,id,requirement),(row,id,requirement))
    # item1 = (row,id,requirement)

    # Method that solves all kind of conflict
    def solve_conflict(self, conflict_type="", item1=None, item2=None, choice=None):
        if conflict_type == "redundancy":
            return self.solve_redundancy(item1, item2, choice)
        elif conflict_type == "similarity":
            return self.solve_similarity(item1, item2, choice)
        elif conflict_type == "contradiction":
            return self.solve_contradiction(item1, item2, choice)
        elif conflict_type == "ambiguity":
            return self.solve_ambiguity(item1[2])
        elif conflict_type == "incomplete":
            return self.solve_incomplete()
        else:
            return None

    # Method to solve conflict by choice
    def resolve_by_choice(self, item1=None, item2=None, choice=None):
        if choice == item1:
            return item1
        elif choice == item2:
            return item2
        else:
            return None

    # Method to solve redundancy
    def solve_redundancy(self, item1=None, item2=None, choice=None):
        return self.resolve_by_choice(item1, item2, choice)

    # Method to solve similarity
    def solve_similarity(self, item1=None, item2=None, choice=None):
        return self.resolve_by_choice(item1, item2, choice)

    # Method to solve contradiction
    def solve_contradiction(self, item1=None, item2=None, choice=None):
        return self.resolve_by_choice(item1, item2, choice)
    
    # Method to solve ambiguity
    def solve_ambiguity(self, sentence):
        return self.spacy.replace_vague_with_strong(sentence)
    
    # Method to solve incomplete sentence
    def solve_incomplete(self):
        # This will be solved by deletion in the requirement list in ui instead of here.
        # This serves as a placeholder for expanding development
        return True
    
    # Method to separate pair of conflict by choosing which one to keep
    def seperate_items(self,conflict_pair=(),item_num=None):
        item1, item2 = conflict_pair

        if item_num == 1:
            return item1
        elif item_num == 2:
            return item2
        else:
            return None 
