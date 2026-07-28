import os
import requests
import feedparser

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

def get_news():
    url = "https://news.google.com/rss/search?q=palm+oil"
    feed = feedparser.parse(url)

    news = []

    for item in feed.entries[:5]:
        news.append("📰 " + item.title)

    return news

news = get_news()

if news:
    message = "🌴 FCPO NEWS TEST\n\n"
    message += "\n".join(news)
else:
    message = "❌ RSS tidak memberi berita."

send_telegram(message)
