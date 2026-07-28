import os
import requests
import feedparser

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

feeds = [
    "https://news.google.com/rss/search?q=Malaysia+palm+oil",
    "https://news.google.com/rss/search?q=FCPO+palm+oil"
]

keywords = [
    "palm oil",
    "fcpo",
    "crude palm oil",
    "malaysia palm",
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

        for item in data.entries[:10]:
            title = item.title.lower()

            if any(k in title for k in keywords):
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
