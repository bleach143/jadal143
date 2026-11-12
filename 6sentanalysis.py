from textblob import TextBlob
import pandas as pd

# Sample customer reviews
reviews = [
    "This product is amazing! I love it.",
    "Poor quality, waste of money.",
    "Average product, nothing special.",
    "Excellent service and great product!",
    "Terrible experience, would not recommend."
]

def analyze_sentiment_textblob(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return 'Positive'
    elif polarity < -0.1:
        return 'Negative'
    else:
        return 'Neutral'

# Analyze reviews
results = []
for review in reviews:
    sentiment = analyze_sentiment_textblob(review)
    polarity = TextBlob(review).sentiment.polarity
    results.append({
        'review': review,
        'sentiment': sentiment,
        'polarity': polarity
    })

df = pd.DataFrame(results)
print(df)
