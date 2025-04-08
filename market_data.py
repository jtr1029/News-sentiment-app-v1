import yfinance as yf
import pandas as pd

def get_market_data(ticker, start, end):
    data = yf.download(ticker, start=start, end=end)
    data.reset_index(inplace=True)

    # Flatten column index if MultiIndex exists
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = ['_'.join(col).strip('_') for col in data.columns.values]

    data = data[['Date', f'Close_{ticker}']]
    data.rename(columns={f'Close_{ticker}': 'market_close'}, inplace=True)
    return data
