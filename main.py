import os
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )


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
        "stock price"
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
        "demand",
        "china",
        "india"
    ]


    for item in feed.entries[:30]:

        title = item.title
        lower = title.lower()

        if any(x in lower for x in blacklist):
            continue

        if any(x in lower for x in keywords):
            news.append(title)


    return news[:5]


def analyse_market(news):

    text = " ".join(news).lower()


    bullish_terms = {
        "demand": "Permintaan minyak sawit kukuh",
        "biodiesel": "Sokongan daripada permintaan biodiesel",
        "export": "Eksport sawit memberi sokongan",
        "rise": "Harga menunjukkan kenaikan",
        "gain": "Momentum kenaikan meningkat",
        "support": "Faktor sokongan harga",
        "inventory fall": "Inventori berkurangan"
    }


    bearish_terms = {
        "fall": "Tekanan penurunan harga",
        "decline": "Momentum lemah",
        "weak": "Sentimen pasaran melemah",
        "pressure": "Tekanan jualan meningkat",
        "inventory rise": "Inventori meningkat",
        "crude oil": "Pergerakan minyak mentah memberi tekanan",
        "lower": "Harga lebih rendah"
    }


    bullish = []
    bearish = []


    for key, value in bullish_terms.items():
        if key in text:
            bullish.append(value)


    for key, value in bearish_terms.items():
        if key in text:
            bearish.append(value)


    score = 50 + (len(bullish) * 8) - (len(bearish) * 8)


    if score > 65:
        sentiment = "🟢 BULLISH"
        bias = "Buy on weakness"

    elif score < 40:
        sentiment = "🔴 BEARISH"
        bias = "Sell on rally"

    else:
        sentiment = "🟡 NEUTRAL"
        bias = "Tunggu pengesahan"


    score = max(0, min(score, 100))


    return sentiment, score, bias, bullish, bearish



news = get_fcpo_news()


if news:

    sentiment, score, bias, bullish, bearish = analyse_market(news)


    message = (
        "🌴 FCPO FUNDAMENTAL REPORT\n"
        f"📅 {datetime.now().strftime('%d-%m-%Y %H:%M')}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "📰 BERITA UTAMA\n\n"
    )


    for item in news:
        message += "• " + item + "\n\n"


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


    if score > 65:
        message += "Momentum fundamental menyokong kenaikan FCPO."

    elif score < 40:
        message += "Tekanan fundamental masih menguasai FCPO."

    else:
        message += "Pasaran bercampur. Tunggu pengesahan arah."


    message += "\n\n⏰ Update automatik setiap jam"


else:

    message = (
        "🌴 FCPO FUNDAMENTAL REPORT\n\n"
        "Tiada berita utama FCPO ditemui."
    )


send_telegram(message)
