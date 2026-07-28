import os
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime


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
        "FCPO OR crude palm oil OR Malaysian palm oil OR MPOB OR palm oil export OR biodiesel"
    )

    url = f"https://news.google.com/rss/search?q={query}"

    feed = feedparser.parse(url)

    news = []

    blacklist = [
        "indicator",
        "signal",
        "calendar",
        "history",
        "course",
        "explained",
        "technical analysis"
    ]


    for item in feed.entries[:30]:

        title = item.title
        lower = title.lower()

        if any(word in lower for word in blacklist):
            continue

        news.append(title)


    return news[:5]


def translate_basic(text):

    translation = {
        "Palm Oil": "Minyak Sawit",
        "palm oil": "minyak sawit",
        "Crude Palm Oil": "Minyak Sawit Mentah",
        "crude palm oil": "minyak sawit mentah",
        "prices rise": "harga meningkat",
        "prices fall": "harga menurun",
        "rise": "meningkat",
        "rises": "meningkat",
        "gain": "kenaikan",
        "gains": "kenaikan",
        "decline": "penurunan",
        "declines": "menurun",
        "fall": "jatuh",
        "falls": "menurun",
        "weaker": "melemah",
        "stronger": "mengukuh",
        "demand": "permintaan",
        "supply": "bekalan",
        "inventory": "inventori",
        "export": "eksport",
        "exports": "eksport",
        "biodiesel": "biodiesel",
        "Indonesia": "Indonesia",
        "Malaysia": "Malaysia"
    }

    result = text

    for eng, bm in translation.items():
        result = result.replace(eng, bm)

    return result


def analyse(news):

    text = " ".join(news).lower()


    bullish = []
    bearish = []


    bullish_words = {
        "biodiesel": "Permintaan biodiesel menyokong harga FCPO",
        "strong demand": "Permintaan minyak sawit kekal kukuh",
        "tightening supply": "Bekalan semakin ketat",
        "export": "Eksport sawit memberi sokongan",
        "rise": "Momentum kenaikan harga"
    }


    bearish_words = {
        "weaker crude": "Kelemahan minyak mentah memberi tekanan",
        "decline": "Tekanan penurunan harga",
        "fall": "Harga mengalami tekanan",
        "inventory rise": "Inventori meningkat",
        "weak demand": "Permintaan melemah"
    }


    score = 50


    for word, reason in bullish_words.items():

        if word in text:
            score += 10
            bullish.append(reason)


    for word, reason in bearish_words.items():

        if word in text:
            score -= 10
            bearish.append(reason)


    score = max(0, min(score, 100))


    if score >= 65:
        sentiment = "🟢 BULLISH"
        bias = "Cari peluang BUY ketika retracement"

    elif score <= 35:
        sentiment = "🔴 BEARISH"
        bias = "Berhati-hati dengan tekanan SELL"

    else:
        sentiment = "🟡 NEUTRAL"
        bias = "Tunggu pengesahan arah"


    return sentiment, score, bias, bullish, bearish



news = get_fcpo_news()


if news:

    sentiment, score, bias, bullish, bearish = analyse(news)


    message = (
        "🌴 LAPORAN FUNDAMENTAL FCPO\n"
        f"📅 {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "📰 BERITA UTAMA\n\n"
    )


    for item in news:
        message += "• " + translate_basic(item) + "\n\n"


    message += (
        "━━━━━━━━━━━━━━\n\n"
        "📊 SENTIMEN PASARAN FCPO\n\n"
        f"{sentiment}\n"
        f"Skor: {score}/100\n"
        f"Bias: {bias}\n\n"
        "━━━━━━━━━━━━━━\n\n"
    )


    message += "🟢 FAKTOR SOKONGAN\n\n"

    if bullish:
        for item in bullish:
            message += "✅ " + item + "\n"
    else:
        message += "• Tiada faktor sokongan kuat dikesan\n"


    message += "\n🔴 FAKTOR TEKANAN\n\n"

    if bearish:
        for item in bearish:
            message += "⚠️ " + item + "\n"
    else:
        message += "• Tiada tekanan besar dikesan\n"


    message += (
        "\n━━━━━━━━━━━━━━\n\n"
        "🎯 KESIMPULAN TRADER\n\n"
    )


    if score >= 65:
        message += "Fundamental FCPO menunjukkan sokongan kenaikan."

    elif score <= 35:
        message += "Fundamental FCPO menunjukkan tekanan penurunan."

    else:
        message += "Pasaran FCPO masih bercampur dan memerlukan pengesahan."


    message += "\n\n⏰ Kemas kini automatik setiap jam"


else:

    message = (
        "🌴 LAPORAN FUNDAMENTAL FCPO\n\n"
        "Tiada berita utama ditemui."
    )


send_telegram(message)
