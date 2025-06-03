import spacy
import random

# Class to implement spacy
class SpacyImplementation:
    def __init__(self):
        # Create a blank English nlp object
        self.nlp = spacy.blank("en")

        # load english (large) package
        self.nlp = spacy.load("en_core_web_lg")

        # Keywords for word checking
        self.negative_keywords = ["must not", "should not", "cannot", "never", "no", "not allowed", "not"]
        self.vague_keywords = ["maybe", "might", "could"]
        self.strong_keywords = ["shall", "will", "should", "may"]

        # Below are unimplemented keywords that can be used in future developments
        # self.vague_keywords = [""
        #     "maybe", "may", "might", "could", "some", "somewhat", "roughly", "around", "quickly", "strongly", 
        #     "vaguely", "a bit", "few"
        #     ""]

    # Method to checkif spacy is running
    def is_spacy_running(self):
        doc = "This is to test if Spacy can be run."
        try:
            doc = self.nlp(doc)
            print("Spacy is running.")
        except:
            print("Spacy fails to run.")

    # Method to get natural language processing (nlp)
    def get_nlp(self, text):
        return self.nlp(text)   

    # Method to implement Spacy similarity check between two sentence
    def spacy_similarity(self,sentence1="", sentence2=""):
        return sentence1.similarity(sentence2)

    # Method to check if two sentences are redundant (exactly the same)
    def redundancy_check(self, similarity=0.0):
        return similarity == 1

    # Method to check if two sentences are very similar 
    def similarity_check(self, similarity=0.0):
        return similarity > 0.9490 and similarity < 1.0

    # Method to check if one sentence is negating the other sentence
    def contradiction_check(self, similarity=0.0, sentence1="", sentence2=""):
        has_neg1 = any(neg in sentence1  for neg in self.negative_keywords)
        has_neg2 = any(neg in sentence2  for neg in self.negative_keywords)
        if similarity > 0.9490 and similarity < 1.0:
            if has_neg1 != has_neg2:
                return True
        else :
            return False    
        
    # Method to check if theres ambigious words in sentence
    def ambiguity_check(self, sentence=""):
        if any(vague in sentence for vague in self.vague_keywords) == True:
            return True
        else:
            return False

    # Method to check if sentence seems incomplete    
    def incomplete_check(self, sentence=""):
        if self.is_incomplete(sentence) == True:
            return True
        else:
            return False

    # Method to replace a word with another word   
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

    # Method to replace vague word with strong words  
    def replace_vague_with_strong(self, sentence=""):
        sentence = self.nlp(sentence)
        new_sentence = sentence
        with_word = random.choice(self.strong_keywords)

        for word in sentence:
            if word.text.lower() in self.vague_keywords:
                new_sentence = self.replace_word(sentence, word.text, with_word)

        return new_sentence

    # Method to see if sentence is incomplete
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

