import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def merge_data(sentiment_df, market_df):
    print("Sentiment columns:", sentiment_df.columns)
    print("Market columns:", market_df.columns)
    print("Sentiment dtypes:\n", sentiment_df.dtypes)
    print("Market dtypes:\n", market_df.dtypes)
    merged = pd.merge(sentiment_df, market_df, on='Date', how='inner')
    return merged


def plot_comparison(merged_df, dual_axis=False, simplify_dates=False, smooth=False):
    fig, ax1 = plt.subplots(figsize=(10, 5))

    x = merged_df['Date']
    y1 = merged_df['sentiment']
    y2 = merged_df['market_close']

    ax1.plot(x, y1, color='tab:blue', label='Sentiment Score')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Sentiment Score', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    if simplify_dates:
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        fig.autofmt_xdate()

    if dual_axis:
        ax2 = ax1.twinx()
        ax2.plot(x, y2, color='tab:orange', label='Market Close')
        ax2.set_ylabel('Market Close', color='tab:orange')
        ax2.tick_params(axis='y', labelcolor='tab:orange')
    else:
        ax1.plot(x, y2, color='tab:orange', label='Market Close')

    plt.title('Sentiment vs Market Movement')
    fig.tight_layout()
    return fig


def plot_sentiment_distribution(scored_df):
    plt.figure(figsize=(8, 4))
    plt.hist(scored_df['sentiment'], bins=20, color='skyblue', edgecolor='black')
    plt.title("Distribution of Sentiment Scores")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    return plt


def plot_sentiment_timeseries(aggr_df):
    plt.figure(figsize=(10, 4))
    plt.plot(aggr_df['Date'], aggr_df['sentiment'], color='green', label='Daily Avg Sentiment')
    plt.title("Sentiment Scores Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Sentiment")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt
