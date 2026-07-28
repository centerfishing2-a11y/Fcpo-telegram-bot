import os
import requests
import feedparser

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

feeds = [
    "https://news.google.com/rss/search?q=palm+oil+Malaysia",
    "https://news.google.com/rss/search?q=crude+palm+oil",
    "https://news.google.com/rss/search?q=FCPO",
    "https://news.google.com/rss/search?q=Malaysian+palm+oil+futures"
]

keywords = [
    "palm",
    "oil",
    "fcpo",
    "cpo",
    "malaysia",
    "mpob"
]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

def get_fcpo_news():
    result = []

    for feed in feeds:
        data = feedparser.parse(feed)

        for item in data.entries[:5]:
            result.append(item.title)

    return result[:5]

news = get_fcpo_news()

if news:
    msg = "🌴 FCPO FUNDAMENTAL UPDATE\n\n"

    for item in news:
        msg += "📰 " + item + "\n\n"

else:
    msg = "🌴 FCPO FUNDAMENTAL UPDATE\n\nTiada berita FCPO terbaru ditemui."

send_telegram(msg)
