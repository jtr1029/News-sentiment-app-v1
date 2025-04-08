import pandas as pd
from textblob import TextBlob


def score_sentiment(text):
    if not isinstance(text, str):
        return 0.0
    return TextBlob(text).sentiment.polarity


def process_news_dataframe(df):
    df['sentiment'] = df['text'].apply(score_sentiment)
    return df


### app/aggregation.py
import pandas as pd

def aggregate_sentiment(df, time_col='date'):
    df[time_col] = pd.to_datetime(df[time_col])
    return df.groupby(df[time_col].dt.date)['sentiment'].mean().reset_index()
