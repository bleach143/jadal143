import nltk
from nltk.tokenize import word_tokenize

# Sample text
text = "The quick brown fox jumps over the lazy dog"
tokens = word_tokenize(text)

# POS tagging
pos_tags = nltk.pos_tag(tokens)

print("POS Tags:", pos_tags)

# Explanation of common POS tags
pos_explanations = {
    'DT': 'Determiner',
    'JJ': 'Adjective',
    'NN': 'Noun, singular',
    'NNS': 'Noun, plural',
    'VBZ': 'Verb, 3rd person singular present',
    'IN': 'Preposition',
    'RB': 'Adverb'
}

for word, pos in pos_tags:
    explanation = pos_explanations.get(pos, 'Other')
    print(f"{word}: {pos} ({explanation})")
