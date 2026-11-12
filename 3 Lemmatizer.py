import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Sample text
text = "running runs ran runner easily fairly better"
tokens = word_tokenize(text)

# Apply lemmatization without POS
lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]

print("Original words:", tokens)
print("Lemmatized words:", lemmatized_words)

# With POS tagging for better results
pos_tags = nltk.pos_tag(tokens)
lemmatized_with_pos = []

for word, pos in pos_tags:
    if pos.startswith('V'):
        lemmatized_with_pos.append(lemmatizer.lemmatize(word, pos='v'))
    elif pos.startswith('N'):
        lemmatized_with_pos.append(lemmatizer.lemmatize(word, pos='n'))
    elif pos.startswith('R'):
        lemmatized_with_pos.append(lemmatizer.lemmatize(word, pos='r'))
    elif pos.startswith('J'):  # Adjective
        lemmatized_with_pos.append(lemmatizer.lemmatize(word, pos='a'))
    else:
        lemmatized_with_pos.append(lemmatizer.lemmatize(word))

print("Lemmatized with POS:", lemmatized_with_pos)
