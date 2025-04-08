import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def score_sentiment(text):
    if not isinstance(text, str):
        return 0.0
    score = analyzer.polarity_scores(text)
    return score['compound']

def process_news_dataframe(df):
    df['sentiment'] = df['text'].apply(score_sentiment)
    return df
