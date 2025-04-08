import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

analyzer = SentimentIntensityAnalyzer()

def score_sentiment(text):
    if not isinstance(text, str):
        return 0.0
    score = analyzer.polarity_scores(text)
    return score['compound']

def process_news_dataframe(df):
    df['sentiment'] = df['text'].apply(score_sentiment)
    return df
