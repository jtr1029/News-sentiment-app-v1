import os
import subprocess
import sys

# Try to import, if fail, install and reload
try:
    from textblob import TextBlob
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "textblob"])
    from textblob import TextBlob

import streamlit as st
import pandas as pd
import config
import utils
import sentiment_analysis
import aggregation
import market_data
import analysis

st.title("📈 News Sentiment vs Market Risk")

ticker = st.text_input("Enter stock ticker:", value=config.DEFAULT_TICKER)
date_range = st.date_input("Select date range:", value=config.DEFAULT_DATE_RANGE)

# Simulated News Data
sample_news = pd.DataFrame({
    'date': pd.date_range(date_range[0], periods=5),
    'text': [
        "Stock prices soar as investors gain confidence.",
        "The market experiences slight corrections amid inflation fears.",
        "Tech stocks rally after strong earnings reports.",
        "Analysts warn of possible downturn due to rate hikes.",
        "Investors remain optimistic despite mixed signals."
    ]
})

scored_df = sentiment_analysis.process_news_dataframe(sample_news)
aggr_df = aggregation.aggregate_sentiment(scored_df)

market_df = market_data.get_market_data(ticker, *date_range)
merged_df = analysis.merge_data(aggr_df, market_df)

st.subheader("Sentiment and Market Close Over Time")
fig = analysis.plot_comparison(merged_df)
st.pyplot(fig)

st.subheader("Raw Sentiment Data")
st.dataframe(scored_df)

st.subheader("Aggregated Sentiment")
st.dataframe(aggr_df)

st.subheader("Market Data")
st.dataframe(market_df)
