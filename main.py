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
        "FCPO OR crude palm oil OR Malaysian palm oil futures OR MPOB"
    )

    url = f"https://news.google.com/rss/search?q={query}"

    feed = feedparser.parse(url)

    news = []

    remove_words = [
        "indicator",
        "explained",
        "how to",
        "education",
        "course"
    ]

    keep_words = [
        "fcpo",
        "palm oil",
        "crude palm oil",
        "malaysia",
        "mpob",
        "futures",
        "export",
        "inventory"
    ]


    for item in feed.entries[:15]:

        title = item.title
        lower = title.lower()

        if any(x in lower for x in remove_words):
            continue

        if any(x in lower for x in keep_words):
            news.append(title)


    return news[:5]


def translate_title(title):

    # Terjemahan asas untuk perkataan yang biasa keluar FCPO

    replacements = {
        "prices": "harga",
        "price": "harga",
        "could retest": "berpotensi menguji semula",
        "bearish momentum": "momentum penurunan",
        "bullish momentum": "momentum kenaikan",
        "rises": "meningkat",
        "falls": "menurun",
        "declines": "merosot",
        "higher": "lebih tinggi",
        "lower": "lebih rendah",
        "palm oil": "minyak sawit",
        "crude palm oil": "minyak sawit mentah",
        "exports": "eksport",
        "inventory": "inventori"
    }

    result = title

    for eng, bm in replacements.items():
        result = result.replace(eng, bm)

    return result


news = get_fcpo_news()


if news:

    message = "🌴 KEMASKINI FUNDAMENTAL FCPO\n\n"

    for item in news:
        bm = translate_title(item)
        message += "📰 " + bm + "\n\n"

else:

    message = (
        "🌴 KEMASKINI FUNDAMENTAL FCPO\n\n"
        "Tiada berita FCPO terbaru ditemui."
    )


send_telegram(message)
