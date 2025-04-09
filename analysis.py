from sklearn.linear_model import LinearRegression

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

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

def calculate_sentiment_volatility(scored_df, window=5):
    scored_df = scored_df.copy()
    scored_df['date'] = pd.to_datetime(scored_df['date'])

    daily_sentiment = scored_df.groupby('date')['sentiment'].mean().reset_index()
    daily_sentiment['sentiment_volatility'] = daily_sentiment['sentiment'].rolling(window=window).std()

    return daily_sentiment

def plot_sentiment_volatility(scored_df):
    df = calculate_sentiment_volatility(scored_df)
    df = df.dropna(subset=['sentiment_volatility'])

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['date'], df['sentiment_volatility'], color='slateblue', linewidth=2)
    ax.set_title("Sentiment Volatility (5-Day Rolling Std Dev)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    fig.tight_layout()
    return fig

def calculate_beta(stock_returns, benchmark_returns):
    df = pd.DataFrame({
        'stock': stock_returns,
        'benchmark': benchmark_returns
    }).dropna()

    X = df['benchmark'].values.reshape(-1, 1)
    y = df['stock'].values

    model = LinearRegression().fit(X, y)
    beta = model.coef_[0]
    alpha = model.intercept_
    return beta, alpha

def compute_daily_returns(price_df):
    price_df = price_df.sort_values('Date')
    returns = price_df.set_index('Date')['market_close'].pct_change().dropna()
    return returns

def calculate_sentiment_beta(aggr_sentiment_df, market_df):
    aggr_sentiment_df = aggr_sentiment_df.copy()
    market_df = market_df.copy()
    aggr_sentiment_df['Date'] = pd.to_datetime(aggr_sentiment_df['Date'])
    market_df['Date'] = pd.to_datetime(market_df['Date'])

    market_df['returns'] = market_df['market_close'].pct_change()
    df = pd.merge(aggr_sentiment_df, market_df[['Date', 'returns']], on='Date', how='inner')
    df = df.dropna()

    X = df[['returns']]
    y = df['sentiment']

    model = LinearRegression().fit(X, y)
    sentiment_beta = model.coef_[0]
    sentiment_alpha = model.intercept_
    return sentiment_beta, sentiment_alpha

def calculate_conditional_var(sentiment_df, alpha=0.05):
    if sentiment_df.empty or 'sentiment' not in sentiment_df.columns:
        return None, None, None

    sentiment_df = sentiment_df.copy()
    sentiment_df['date'] = pd.to_datetime(sentiment_df['date'])
    daily_returns = sentiment_df.groupby('date')['sentiment'].mean()

    sorted_returns = daily_returns.sort_values()
    cutoff_index = int(len(sorted_returns) * alpha)

    if cutoff_index < 1:
        return None, None, None

    var = sorted_returns.iloc[cutoff_index]
    cvar = sorted_returns.iloc[:cutoff_index].mean()
    std_dev = sorted_returns.std()

    return var, cvar, std_dev
