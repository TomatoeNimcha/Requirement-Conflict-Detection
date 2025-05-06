import spacy

class SpacyImplementation:
    def __init__(self):
        # Create a blank English nlp object
        self.nlp = spacy.blank("en")

        # load english(large) package
        self.nlp = spacy.load("en_core_web_lg")

        self.negative_keywords = ["must not", "should not", "cannot", "never", "no", "not allowed"]


    def redundancy_check(self, sentence1="", sentence2=""):
        sentence1 = self.nlp(sentence1)
        sentence2 = self.nlp(sentence2)

        similarity = sentence1.similarity(sentence2)
        print(f"Similarity: {similarity:.4f}")

        if similarity  == 1 : 
            print("Redundant")
            return True
            
        else :
            print("Not redundant")
            return False

    def similarity_check(self, sentence1="", sentence2=""):
        sentence1 = self.nlp(sentence1)
        sentence2 = self.nlp(sentence2)

        similarity = sentence1.similarity(sentence2)
        print(f"Similarity: {similarity:.4f}")

        if similarity > 0.9009 and similarity < 0.99: #Similarity index, the control of how similar it is
            print("Similar")
            return True
            
        else :
            print("Not similarity")
            return False

    def contradiction_check(self, sentence1="", sentence2=""):
        has_neg1 = any(neg in sentence1 for neg in self.negative_keywords)
        has_neg2 = any(neg in sentence2 for neg in self.negative_keywords)

        sentence1 = self.nlp(sentence1)
        sentence2 = self.nlp(sentence2)

        similarity = sentence1.similarity(sentence2)
        print(f"Similarity: {similarity:.4f}")

        if similarity > 0.9009 and similarity != 1.0:
            if has_neg1 != has_neg2:
                print("Contradicticting")
                return True
        else :
            print("Not contradction") 
            return False       
        
# test = SpacyImplementation()


# test.contradiction_check("The user shall log in", "The user shall not log in")
# test.contradiction_check("The user shall log in", "The user shall log in")
# test.similarity_check("The user shall log in", "The user shall log in")
# test.redundancy_check("The user shall log in", "The user shall log in")


# test.similarityCheck("The user shall log in", "The user shall sign out")
# test.similarityCheck("The user shall be able to reset their password via email.", 
#                      "The admin shall approve or reject submitted content.")
# test.similarityCheck("The system shall notify users when a new message is received.", 
#                      "When the form is submitted, the system shall notify users when a new message is received.")

