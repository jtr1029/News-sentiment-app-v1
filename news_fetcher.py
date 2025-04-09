import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(ticker, from_date, to_date, max_articles=100):
    query = f'"{ticker}"'
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={query}&from={from_date}&to={to_date}"
        f"&language=en&sortBy=publishedAt&pageSize=100&apiKey={API_KEY}"
    )

    print("🔍 URL being requested:", url)

    response = requests.get(url)
    if response.status_code != 200:
        print("❌ API request failed:", response.text)
        return pd.DataFrame()

    articles = response.json().get("articles", [])
    if not articles:
        print("⚠️ No articles found.")
        return pd.DataFrame()

    # Build dataframe
    records = []
    for article in articles[:max_articles]:
        published_at = article.get("publishedAt", "")
        title = article.get("title", "")
        if published_at and title:
            records.append({
                "date": published_at[:10],  # Just the YYYY-MM-DD
                "text": title
            })

    df = pd.DataFrame(records)
    print("✅ Sample news DataFrame preview:")
    print(df.head())
    return df
