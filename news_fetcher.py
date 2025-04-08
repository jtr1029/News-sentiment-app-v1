import requests
import pandas as pd
import os
import .env
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(ticker, from_date, to_date, max_articles=100):
    query = f'"{ticker}"'
    url = (
        f"https://newsapi.org/v2/everything?q={query}"
        f"&from={from_date}&to={to_date}&language=en&sortBy=publishedAt"
        f"&pageSize=100&apiKey={API_KEY}"
    )

    response = requests.get(url)
    articles = response.json().get("articles", [])

    # DEBUG
    if not articles:
        print("⚠️ No articles returned from NewsAPI.")

    data = []
    for article in articles[:max_articles]:
        data.append({
            "date": article.get("publishedAt", "")[:10],
            "text": article.get("title", "")  # ⬅️ this is CRITICAL
        })

    df = pd.DataFrame(data)
    return df
