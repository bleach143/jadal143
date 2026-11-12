import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import re

def lexical_analysis(text):
    # Basic statistics
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # Remove punctuation
    words = [word for word in words if word.isalpha()]
    
    # Analysis
    num_sentences = len(sentences)
    num_words = len(words)
    num_unique_words = len(set(words))
    avg_word_length = sum(len(word) for word in words) / len(words)
    
    # Word frequency
    word_freq = Counter(words)
    most_common = word_freq.most_common(10)
    
    # Lexical diversity
    lexical_diversity = num_unique_words / num_words
    
    print(f"Number of sentences: {num_sentences}")
    print(f"Number of words: {num_words}")
    print(f"Number of unique words: {num_unique_words}")
    print(f"Average word length: {avg_word_length:.2f}")
    print(f"Lexical diversity: {lexical_diversity:.2f}")
    print(f"Most common words: {most_common}")
    
    return {
        'sentences': num_sentences,
        'words': num_words,
        'unique_words': num_unique_words,
        'avg_word_length': avg_word_length,
        'lexical_diversity': lexical_diversity,
        'word_frequency': word_freq
    }

# Sample text
sample_text = """
Natural language processing is a fascinating field of study. 
It combines computer science, artificial intelligence, and linguistics. 
The goal is to enable computers to understand and process human language.
"""

analysis_results = lexical_analysis(sample_text)
