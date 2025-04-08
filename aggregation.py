import pandas as pd

def aggregate_sentiment(df, time_col='date'):
    df[time_col] = pd.to_datetime(df[time_col])
    result = df.groupby(df[time_col].dt.date)['sentiment'].mean().reset_index()
    result.rename(columns={result.columns[0]: 'Date'}, inplace=True)
    result['Date'] = pd.to_datetime(result['Date'])  # Ensure datetime dtype
    return result
