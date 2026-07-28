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
        "FCPO OR crude palm oil OR Malaysian palm oil OR MPOB OR palm oil export"
    )

    url = f"https://news.google.com/rss/search?q={query}"

    feed = feedparser.parse(url)

    news = []

    blacklist = [
        "indicator",
        "calendar",
        "history",
        "explained",
        "course",
        "signal"
    ]

    for item in feed.entries[:20]:

        title = item.title
        lower = title.lower()

        if any(word in lower for word in blacklist):
            continue

        news.append(title)

    return news[:5]


def analyze_sentiment(news):

    text = " ".join(news).lower()

    bullish = [
        "rise",
        "higher",
        "gain",
        "strong",
        "demand",
        "support",
        "biodiesel",
        "export increase",
        "stock fall",
        "inventory fall"
    ]

    bearish = [
        "fall",
        "lower",
        "decline",
        "weak",
        "pressure",
        "inventory rise",
        "stocks increase",
        "slow demand"
    ]

    bull_score = 0
    bear_score = 0

    bull_reason = []
    bear_reason = []


    for word in bullish:
        if word in text:
            bull_score += 10
            bull_reason.append(word)


    for word in bearish:
        if word in text:
            bear_score += 10
            bear_reason.append(word)


    score = 50 + bull_score - bear_score

    if score > 60:
        sentiment = "🟢 BULLISH"

    elif score < 40:
        sentiment = "🔴 BEARISH"

    else:
        sentiment = "🟡 NEUTRAL"


    return sentiment, score, bull_reason, bear_reason



news = get_fcpo_news()


if news:

    sentiment, score, bull, bear = analyze_sentiment(news)

    message = "🌴 FCPO FUNDAMENTAL UPDATE\n\n"

    message += "📰 Berita Utama:\n\n"

    for item in news:
        message += "• " + item + "\n\n"


    message += (
        "📊 Analisis Sentimen:\n"
        f"{sentiment}\n"
        f"Skor: {score}/100\n\n"
    )


    if bull:
        message += "🟢 Faktor Positif:\n"
        for x in bull:
            message += "• " + x + "\n"

        message += "\n"


    if bear:
        message += "🔴 Faktor Risiko:\n"
        for x in bear:
            message += "• " + x + "\n"


    message += "\n⏰ Update automatik setiap jam"


else:

    message = (
        "🌴 FCPO FUNDAMENTAL UPDATE\n\n"
        "Tiada berita utama ditemui."
    )


send_telegram(message)
