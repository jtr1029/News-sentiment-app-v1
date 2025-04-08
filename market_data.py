import yfinance as yf
import pandas as pd

def get_market_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)
    data = data[['Date', 'Close']]
    data.rename(columns={'Close': 'market_close'}, inplace=True)
    return data
