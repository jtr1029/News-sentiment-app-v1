import streamlit as st
import pandas as pd
import config
import utils
import sentiment_analysis
import aggregation
import market_data
import analysis

import random

st.title("📈 News Sentiment vs Market Risk")

ticker = st.text_input("Enter stock ticker:", value=config.DEFAULT_TICKER)
date_range = st.date_input("Select date range:", value=config.DEFAULT_DATE_RANGE)

# Simulated News Data - one random statement per day
random_texts = [
    "Stocks surge as market optimism grows.",
    "Economic uncertainty dampens investor sentiment.",
    "Technology shares rally after earnings reports.",
    "Market struggles with inflation concerns.",
    "Analysts predict a bullish trend.",
    "Investors cautious ahead of Fed meeting."
]
date_index = pd.date_range(date_range[0], date_range[1])
news_texts = [random.choice(random_texts) for _ in range(len(date_index))]

sample_news = pd.DataFrame({
    'date': date_index,
    'text': news_texts
})

scored_df = sentiment_analysis.process_news_dataframe(sample_news)
aggr_df = aggregation.aggregate_sentiment(scored_df)
market_df = market_data.get_market_data(ticker, *date_range)

# Display news with sentiment scores
st.subheader("Scored News Headlines")
st.dataframe(scored_df[['date', 'text', 'sentiment']])

# 🎯 Plot sentiment distribution
st.subheader("Distribution of Individual Sentiment Scores")
dist_plot = analysis.plot_sentiment_distribution(scored_df)
st.pyplot(dist_plot)

# 📊 Plot sentiment over time
st.subheader("Aggregated Sentiment Over Time")
sentiment_time_plot = analysis.plot_sentiment_timeseries(aggr_df)
st.pyplot(sentiment_time_plot)

# ⛓ Merge and plot
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

