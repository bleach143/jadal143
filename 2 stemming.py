from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Initialize stemmer
stemmer = PorterStemmer()

# Sample text
text = "running runs ran runner easily fairly"
tokens = word_tokenize(text)

# Apply stemming
stemmed_words = [stemmer.stem(word) for word in tokens]

print("Original words:", tokens)
print("Stemmed words:", stemmed_words)
