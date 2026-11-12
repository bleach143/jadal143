# Initial NLTK Setup
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')
nltk.download('punkt_tab')


# Lab 1a: Stopword Elimination
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Sample text
text = "This is a sample document for text preprocessing. We will remove stopwords from this text."

# Tokenize the text
tokens = word_tokenize(text.lower())

# Get English stopwords
stop_words = set(stopwords.words('english'))

# Remove stopwords
filtered_tokens = [word for word in tokens if word not in stop_words and word.isalpha()]

print("Original tokens:", tokens)
print("Filtered tokens:", filtered_tokens)
