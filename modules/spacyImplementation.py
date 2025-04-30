import spacy

class SpacyImplementation:
    def __init__(self):
        # Create a blank English nlp object
        self.nlp = spacy.blank("en")

        # load english(large) package
        self.nlp = spacy.load("en_core_web_lg")

    def similarityCheck(self, sentence1="", sentence2=""):
        sentence1 = self.nlp(sentence1)
        sentence2 = self.nlp(sentence2)

        similarity = sentence1.similarity(sentence2)
        print(f"Similarity: {similarity:.4f}")

        if similarity > 0.9009 : #Similarity index, the control of how similar it is
            print("Similar")
            return True
            
        else :
            print("Not similar")
            return False
        
        
# test = spacyImplementation()

# test.similarityCheck("The user shall log in", "The user shall log in")
# test.similarityCheck("The user shall log in", "The user shall sign out")
# test.similarityCheck("The user shall be able to reset their password via email.", 
#                      "The admin shall approve or reject submitted content.")
# test.similarityCheck("The system shall notify users when a new message is received.", 
#                      "When the form is submitted, the system shall notify users when a new message is received.")

