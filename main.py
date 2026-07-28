import os
import requests
import feedparser

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)


def get_fcpo_news():
    feeds = [
        "https://news.google.com/rss/search?q=FCPO",
        "https://news.google.com/rss/search?q=crude+palm+oil",
        "https://news.google.com/rss/search?q=Malaysian+palm+oil"
    ]

    keywords = [
        "fcpo",
        "crude palm oil",
        "palm oil futures",
        "malaysian palm oil",
        "mpob"
    ]

    news = []

    for url in feeds:
        feed = feedparser.parse(url)

        for item in feed.entries[:10]:
            title = item.title

            if any(word in title.lower() for word in keywords):
                news.append("📰 " + title)

    return news[:5]


news = get_fcpo_news()


if news:
    message = "🌴 FCPO FUNDAMENTAL UPDATE\n\n"
    
    for item in news:
        message += item + "\n\n"

else:
    message = "🌴 FCPO FUNDAMENTAL UPDATE\n\nTiada berita FCPO terbaru ditemui."


send_telegram(message)
