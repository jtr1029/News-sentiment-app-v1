import pandas as pd
import matplotlib.pyplot as plt

def merge_data(sentiment_df, market_df):
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])  # Already renamed in aggregation
    market_df['date'] = pd.to_datetime(market_df['date'])
    merged = pd.merge(sentiment_df, market_df, on='date', how='inner')
    return merged


def plot_comparison(merged_df):
    plt.figure(figsize=(10,5))
    plt.plot(merged_df['Date'], merged_df['sentiment'], label='Sentiment Score')
    plt.plot(merged_df['Date'], merged_df['market_close'], label='Market Close')
    plt.legend()
    plt.title("Sentiment vs Market Movement")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt
