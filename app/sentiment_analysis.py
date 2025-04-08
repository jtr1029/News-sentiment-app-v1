import pandas as pd
from textblob import TextBlob

def score_sentiment(text):
    if not isinstance(text, str):
        return 0.0
    return TextBlob(text).sentiment.polarity  # Returns value between -1.0 and 1.0

def process_news_dataframe(df):
    df['sentiment'] = df['text'].apply(score_sentiment)
    return df
