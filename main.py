import os
import requests
import feedparser

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def get_news():
    url = "https://news.google.com/rss/search?q=(FCPO OR crude palm oil OR Malaysian palm oil OR palm oil futures)"
    feed = feedparser.parse(url)

    news = []

    for item in feed.entries[:10]:
        title = item.title.lower()

        if any(word in title for word in [
            "fcpo",
            "crude palm oil",
            "palm oil futures",
            "malaysian palm oil",
            "mpob"
        ]):
            news.append("📰 " + item.title)

    return news[:5]

news = get_news()

if news:
   message = "🌴 FCPO FUNDAMENTAL UPDATE\n\n"
   message += "\n".join(news) 
else:
    message = "❌ RSS tidak memberi berita."

send_telegram(message)
