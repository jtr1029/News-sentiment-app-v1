import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

def score_sentiment(text):
    if not isinstance(text, str):
        return 0.0
    return analyzer.polarity_scores(text)['compound']

def process_news_dataframe(df):
    df['sentiment'] = df['text'].apply(score_sentiment)
    return df
