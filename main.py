import os
import requests
import feedparser
from urllib.parse import quote


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })


def get_fcpo_news():

    query = quote(
        "FCPO palm oil Malaysia export inventory production biodiesel"
    )

    url = f"https://news.google.com/rss/search?q={query}"

    feed = feedparser.parse(url)

    news = []

    blacklist = [
        "calendar",
        "indicator",
        "explained",
        "history",
        "course",
        "signal"
    ]

    keywords = [
        "fcpo",
        "palm oil",
        "crude palm oil",
        "malaysia",
        "mpob",
        "export",
        "inventory",
        "production",
        "biodiesel",
        "china",
        "india"
    ]


    for item in feed.entries[:20]:

        title = item.title
        lower = title.lower()

        if any(x in lower for x in blacklist):
            continue

        if any(x in lower for x in keywords):
            news.append(title)


    return news[:5]


def sentiment(news):

    text = " ".join(news).lower()

    bullish_words = [
        "rise",
        "higher",
        "gain",
        "strong",
        "increase",
        "support",
        "demand"
    ]

    bearish_words = [
        "fall",
        "lower",
        "decline",
        "weak",
        "drop",
        "pressure",
        "slow"
    ]


    bull = sum(word in text for word in bullish_words)
    bear = sum(word in text for word in bearish_words)


    if bull > bear:
        return "🟢 BULLISH"

    elif bear > bull:
        return "🔴 BEARISH"

    else:
        return "🟡 NEUTRAL"



news = get_fcpo_news()


if news:

    mood = sentiment(news)

    message = (
        "🌴 KEMASKINI FUNDAMENTAL FCPO\n\n"
    )

    for item in news:
        message += "📰 " + item + "\n\n"

    message += (
        "📊 SENTIMEN FCPO:\n"
        + mood
        + "\n\n⏰ Update automatik setiap jam"
    )

else:

    message = (
        "🌴 KEMASKINI FUNDAMENTAL FCPO\n\n"
        "Tiada berita utama ditemui."
    )


send_telegram(message)
