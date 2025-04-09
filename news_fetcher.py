import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(ticker, from_date, to_date, max_articles=100):
    query = f"{ticker}"
    url = (
        f"https://gnews.io/api/v4/search?"
        f"q={query}&from={from_date}&to={to_date}"
        f"&lang=en&sortby=publishedAt&max={max_articles}&apikey={API_KEY}"
    )

    print("🔍 GNews URL being requested:", url)

    response = requests.get(url)
    if response.status_code != 200:
        print("❌ GNews API request failed:", response.text)
        return pd.DataFrame()

    articles = response.json().get("articles", [])
    if not articles:
        print("⚠️ No articles found.")
        return pd.DataFrame()

    # Build dataframe
    records = []
    for article in articles:
        published_at = article.get("publishedAt", "")
        title = article.get("title", "")
        if published_at and title:
            records.append({
                "date": published_at[:10],  # YYYY-MM-DD
                "text": title
            })

    df = pd.DataFrame(records)
    print("✅ GNews DataFrame preview:")
    print(df.head())
    return df
