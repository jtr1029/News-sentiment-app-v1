import pandas as pd

def aggregate_sentiment(df, time_col='date'):
    df[time_col] = pd.to_datetime(df[time_col])
    return df.groupby(df[time_col].dt.date)['sentiment'].mean().reset_index()
