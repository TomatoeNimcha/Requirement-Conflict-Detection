import spacy
import random

class SpacyImplementation:
    def __init__(self):
        # Create a blank English nlp object
        self.nlp = spacy.blank("en")

        # load english (large) package
        self.nlp = spacy.load("en_core_web_lg")

        # Keywords for word checking
        self.negative_keywords = ["must not", "should not", "cannot", "never", "no", "not allowed", "not"]
        self.vague_keywords = ["maybe", "might", "could"]
        self.strong_keywords = ["shall", "will", "should", "may"] #another word check standard guideline

        # Below are unimplemented keywords that can be used in future developments
        # self.vague_keywords = [""
        #     "maybe", "may", "might", "could", "some", "somewhat", "roughly", "around", "quickly", "strongly", 
        #     "vaguely", "a bit", "few"
        #     ""]


    def is_spacy_running(self):
        doc = "This is to test if Spacy can be run."
        try:
            doc = self.nlp(doc)
            print("Spacy is running.")
        except:
            print("Spacy fails to run.")

    def get_nlp(self, text):
        return self.nlp(text)   

    def spacy_similarity(self,sentence1="", sentence2=""):
        return sentence1.similarity(sentence2)

    def redundancy_check(self, similarity=0.0):
        return similarity == 1

    def similarity_check(self, similarity=0.0):
        return similarity > 0.9490 and similarity < 1.0

    def contradiction_check(self, similarity=0.0, sentence1="", sentence2=""):
        has_neg1 = any(neg in sentence1  for neg in self.negative_keywords)
        has_neg2 = any(neg in sentence2  for neg in self.negative_keywords)
        if similarity > 0.9490 and similarity < 1.0:
            if has_neg1 != has_neg2:
                return True
        else :
            return False    
        
    def ambiguity_check(self, sentence=""):
        if any(vague in sentence for vague in self.vague_keywords) == True:
            return True
        else:
            return False
        
    def incomplete_check(self, sentence=""):
        if self.is_incomplete(sentence) == True:
            return True
        else:
            return False
        
        
    def replace_word(self, sentence="", word="", with_word=""):
        doc = self.nlp(sentence)
        new_tokens = []

        for token in doc:
            if token.text.lower() == word.lower():
                # Replace with new word but keep original spacing
                new_tokens.append(with_word + token.whitespace_)
            else:
                new_tokens.append(token.text_with_ws)

        return "".join(new_tokens)
    
    def replace_vague_with_strong(self, sentence=""):
        sentence = self.nlp(sentence)
        new_sentence = sentence
        with_word = random.choice(self.strong_keywords)

        for word in sentence:
            if word.text.lower() in self.vague_keywords:
                new_sentence = self.replace_word(sentence, word.text, with_word)

        return new_sentence

    def is_incomplete(self, sentence):
        doc = self.get_nlp(sentence)
        
        # If sentence too short its probably incomplete
        if len(doc) < 3:
            return True

        # Check if there's a subject (nsubj = nominal subject)
        has_subject = any(tok.dep_ in ("nsubj", "nsubjpass") for tok in doc)

        # Check if there's a main verb (ROOT verb or auxiliary verb)
        has_verb = any(tok.dep_ == "ROOT" and tok.pos_ in ("VERB", "AUX") for tok in doc)

        # If it's missing either subject or verb, it's probably incomplete
        if not has_subject or not has_verb:
            return True

        # If the sentence ends with conjunction like and, or, its definitely incomplete
        if doc[-1].text.lower() in {"and", "or", "but"}:
            return True

        # If it starts with a marker like "when", "if" and is short, probably incomplete
        if doc[0].dep_ == "mark" and len(doc) < 7:
            return True

        # Otherwise, it seems complete
        return False

        
    

# test = SpacyImplementation()
# print(test.replace_word("I may be gay.", "may", "will"))
# print(test.replace_vague_with_strong("I may be lesbian."))


        


        
# test = SpacyImplementation()

# # doc1 = "The user shall log in"
# # doc2 = "The user shall not log in"
# doc3 = "The user register a second account."
# print(test.ambiguity_check(doc3))


# percentage = test.spacy_similarity(doc1,doc2)
# test.contradiction_check(percentage, "The user shall log in", "The user shall not log in")

# test.contradiction_check("The user shall log in", "The user shall log in")
# test.similarity_check("The user shall log in", "The user shall log in")
# test.redundancy_check("The user shall log in", "The user shall log in")


# test.similarityCheck("The user shall log in", "The user shall sign out")
# test.similarityCheck("The user shall be able to reset their password via email.", 
#                      "The admin shall approve or reject submitted content.")
# test.similarityCheck("The system shall notify users when a new message is received.", 
#                      "When the form is submitted, the system shall notify users when a new message is received.")