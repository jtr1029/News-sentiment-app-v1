import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("86e93cfa23e44affbfabcc6e25334caa")

def fetch_news(ticker, from_date, to_date, max_articles=100):
    query = f'"{ticker}"'
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&from={from_date}&to={to_date}&language=en&sortBy=publishedAt"
        f"&pageSize=100&apiKey={API_KEY}"
    )

    response = requests.get(url)
    articles = response.json().get("articles", [])[:max_articles]

    data = []
    for article in articles:
        data.append({
            "date": article.get("publishedAt", "")[:10],
            "text": article.get("title", "")  # Ensure 'text' is created
        })

    return pd.DataFrame(data)
