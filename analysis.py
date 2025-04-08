import pandas as pd
import matplotlib.pyplot as plt

def merge_data(sentiment_df, market_df):
    print("Sentiment columns:", sentiment_df.columns)
    print("Market columns:", market_df.columns)
    print("Sentiment dtypes:\n", sentiment_df.dtypes)
    print("Market dtypes:\n", market_df.dtypes)
    merged = pd.merge(sentiment_df, market_df, on='Date', how='inner')
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


def plot_sentiment_distribution(scored_df):
    plt.figure(figsize=(8,4))
    plt.hist(scored_df['sentiment'], bins=20, color='skyblue', edgecolor='black')
    plt.title("Distribution of Sentiment Scores")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    return plt


def plot_sentiment_timeseries(aggr_df):
    plt.figure(figsize=(10,4))
    plt.plot(aggr_df['Date'], aggr_df['sentiment'], color='green', label='Daily Avg Sentiment')
    plt.title("Sentiment Scores Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Sentiment")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt
