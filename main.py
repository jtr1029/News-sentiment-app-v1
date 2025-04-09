import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

import config
import utils
import sentiment_analysis
import aggregation
import market_data
import analysis
from news_fetcher import fetch_news

st.title("📈 News Sentiment vs Market Risk")

# Ticker Input
ticker = st.text_input("Enter stock ticker:", value=config.DEFAULT_TICKER)

# Define the last 60 days as the date range
end_date = datetime.today().date()
start_date = end_date - timedelta(days=60)
date_range = (start_date, end_date)

# Cached fetch_news call to reduce API load
@st.cache_data(ttl=3600)
def fetch_news_cached(ticker, start_date, end_date):
    return fetch_news(ticker, start_date, end_date)

# Load news from session or fetch on button press
sample_news = st.session_state.get('sample_news', pd.DataFrame())
if st.button("🔄 Fetch News from GNews API"):
    sample_news = fetch_news_cached(ticker, start_date, end_date)
    st.session_state['sample_news'] = sample_news

# 📰 Show the returned news from API
st.subheader("📰 News Headlines Fetched from GNews API")
st.write("📋 Columns returned:", sample_news.columns.tolist())

# 📈 Calculate Beta and Alpha against benchmark (e.g., S&P 500)
benchmark_ticker = "^GSPC"
benchmark_df = market_data.get_market_data(benchmark_ticker, start_date, end_date)

# 📈 Market data for stock
target_stock_df = market_data.get_market_data(ticker, start_date, end_date)

# Compute daily returns for both stock and benchmark
stock_returns = analysis.compute_daily_returns(target_stock_df)
benchmark_returns = analysis.compute_daily_returns(benchmark_df)

# Calculate beta and alpha
beta, alpha = analysis.calculate_beta(stock_returns, benchmark_returns)

# 📌 Display beta and alpha
st.subheader("Market Risk (Beta & Alpha vs Benchmark)")
st.metric("Beta", round(beta, 3))
st.metric("Alpha", round(alpha, 5))

# 🚫 Handle missing or invalid API response
if sample_news.empty:
    st.warning("No news fetched yet. Click the button above.")
    st.stop()

if 'text' not in sample_news.columns:
    st.error("The news data is missing a 'text' column. Please check the fetch_news function.")
    st.dataframe(sample_news)
    st.stop()

# Preview headlines
st.dataframe(sample_news[['date', 'text']].head())

# 💬 Sentiment scoring
scored_df = sentiment_analysis.process_news_dataframe(sample_news)

# 📉 Sentiment Volatility
st.subheader("Sentiment Volatility (5-Day Rolling Std Dev)")
vol_plot = analysis.plot_sentiment_volatility(scored_df)
st.pyplot(vol_plot)

# 📊 Display scored headlines
st.subheader("Scored News Headlines")
st.dataframe(scored_df[['date', 'text', 'sentiment']])

# 📊 Sentiment distribution
st.subheader("Distribution of Individual Sentiment Scores")
dist_plot = analysis.plot_sentiment_distribution(scored_df)
st.pyplot(dist_plot)

# 📈 Aggregated sentiment over time
aggr_df = aggregation.aggregate_sentiment(scored_df)
