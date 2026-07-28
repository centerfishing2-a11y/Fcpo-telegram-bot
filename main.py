import os
import requests
import feedparser

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

feeds = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://www.investing.com/rss/news_301.rss"
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def get_news():
    news = []

    for feed in feeds:
        data = feedparser.parse(feed)

        for item in data.entries[:3]:
            title = item.title
            if any(word in title.lower() for word in 
                   ["palm", "oil", "commodity", "soybean", "crude"]):
                news.append(title)

    return news[:5]

news = get_news()

if news:
    message = "📰 FCPO FUNDAMENTAL UPDATE\n\n"
    for n in news:
        message += "• " + n + "\n"

    message += "\n📊 Sentimen: Semak arah pasaran berdasarkan berita terkini."
else:
    message = "📰 Tiada berita FCPO utama ditemui."

send_telegram(message)
