#this is spacy
import spacy

# Create a blank English nlp object
nlp = spacy.blank("en")

# Tokenizing the sentence
doc = nlp("Hello, world!")

# Iterate over tokens in a Doc
for token in doc:
    print(token.text)


# Similarity test
nlp = spacy.load("en_core_web_lg")  # make sure to use larger package!
doc1 = nlp("I like salty fries and hamburgers.")
doc2 = nlp("Fast food tastes very good.")
doc3 = nlp("I like salty fries and burgers.")
doc4 = nlp("Today, the world of technology had expanded beyond comprehension!")

# Similarity of two documents
print(doc1, "<->", doc2, doc1.similarity(doc2))
print(doc1, "<->", doc3, doc1.similarity(doc3))
print(doc1, "<->", doc4, doc1.similarity(doc4))
# # Similarity of tokens and spans
# french_fries = doc1[2:4]
# burgers = doc1[5]
# print(french_fries, "<->", burgers, french_fries.similarity(burgers))




