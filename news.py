import feedparser
from urllib.parse import quote

KEYWORDS = [
    "fcpo",
    "palm oil",
    "crude palm oil",
    "cpo",
    "mpob",
    "biodiesel",
    "malaysian palm oil"
]

BLACKLIST = [
    "calendar",
    "indicator",
    "history",
    "course",
    "signal",
    "chart"
]


def get_fcpo_news(limit=5):
    query = quote("FCPO OR palm oil OR crude palm oil OR MPOB OR biodiesel")
    url = (
        f"https://news.google.com/rss/search?"
        f"q={query}&hl=en-US&gl=US&ceid=US:en"
    )

    feed = feedparser.parse(url)

    news = []

    for item in feed.entries:

        title = item.title.strip()
        low = title.lower()

        if not any(k in low for k in KEYWORDS):
            continue

        if any(x in low for x in BLACKLIST):
            continue

        news.append(title)

        if len(news) >= limit:
            break

    return news
