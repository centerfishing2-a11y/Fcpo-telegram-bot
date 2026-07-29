import os
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime, timezone, timedelta


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })


def get_news():
    q = quote("FCPO palm oil Malaysia biodiesel MPOB export inventory")
    url = f"https://google.com{q}"
    feed = feedparser.parse(url)

    result = []
    blacklist = [
        "indicator", "signal", "calendar", "history", 
        "course", "explained"
    ]

    # PENYELARASAN MASA UTC UNTUK JADUAL SETIAP JAM
    waktu_sekarang_utc = datetime.now(timezone.utc)
    # Ditukar kepada 75 minit untuk menampung sela masa 1 jam + delay pelayan GitHub
    had_masa = waktu_sekarang_utc - timedelta(minutes=75)

    for item in feed.entries[:20]:
        title = item.title
        low = title.lower()

        if any(x in low for x in blacklist):
            continue

        if hasattr(item, 'published_parsed') and item.published_parsed:
            waktu_artikel = datetime(*item.published_parsed[:6], tzinfo=timezone.utc)
        else:
            continue

        # Ambil berita yang diterbitkan dalam tempoh 1 jam lepas
        if had_masa < waktu_artikel <= waktu_sekarang_utc:
            result.append(title)

    return result[:5]



def analysis(news):

    text = " ".join(news).lower()

    bull = []
    bear = []

    score = 50


    # Faktor bullish FCPO
    if "stocks expected to fall" in text or "inventory fall" in text:
        score += 15
        bull.append("Inventori sawit dijangka menurun, memberi sokongan kepada harga")

    if "supply outlook tightens" in text or "tightening supply" in text:
        score += 15
        bull.append("Bekalan semakin ketat dan boleh menyokong kenaikan FCPO")

    if "biodiesel" in text:
        score += 10
        bull.append("Permintaan biodiesel meningkatkan penggunaan sawit")

    if "price expected" in text:
        score += 5
        bull.append("Unjuran harga masih menunjukkan sokongan")


    # Faktor bearish FCPO
    if "exports fall" in text or "export decline" in text:
        score -= 10
        bear.append("Eksport menurun memberi tekanan kepada permintaan")

    if "crude oil weaken" in text or "weaker crude" in text:
        score -= 10
        bear.append("Kelemahan minyak mentah boleh menekan sentimen")


    score = max(0, min(score, 100))


    if score >= 65:
        sent = "🟢 BULLISH RINGAN"
        bias = "Cari peluang BUY ketika retracement"

    elif score <= 35:
        sent = "🔴 BEARISH"
        bias = "Berhati-hati dengan tekanan SELL"

    else:
        sent = "🟡 NEUTRAL"
        bias = "Tunggu pengesahan arah"


    return sent, score, bias, bull, bear



news = get_news()


if news:

    sent, score, bias, bull, bear = analysis(news)

    msg = (
        "🌴 LAPORAN FUNDAMENTAL FCPO\n"
        f"📅 {(datetime.now(timezone.utc) + timedelta(hours=8)).strftime('%d-%m-%Y %H:%M')}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "📰 BERITA UTAMA\n\n"
    )


    for n in news:
        msg += "• " + n + "\n\n"


    msg += (
        "━━━━━━━━━━━━━━\n\n"
        "📊 SENTIMEN PASARAN FCPO\n\n"
        f"{sent}\n"
        f"Skor: {score}/100\n"
        f"Bias: {bias}\n\n"
        "━━━━━━━━━━━━━━\n\n"
        "🟢 FAKTOR SOKONGAN\n\n"
    )


    if bull:
        for b in bull:
            msg += "✅ " + b + "\n"
    else:
        msg += "• Tiada faktor kuat dikesan\n"


    msg += "\n🔴 FAKTOR TEKANAN\n\n"

    if bear:
        for b in bear:
            msg += "⚠️ " + b + "\n"
    else:
        msg += "• Tiada tekanan besar dikesan\n"


    msg += (
        "\n━━━━━━━━━━━━━━\n\n"
        "🎯 KESIMPULAN TRADER\n\n"
    )


    if score >= 65:
        msg += "Fundamental lebih menyokong kenaikan FCPO."

    elif score <= 35:
        msg += "Tekanan fundamental masih menguasai FCPO."

    else:
        msg += "Fundamental bercampur. Tunggu pengesahan trend."


    msg += "\n\n⏰ Kemas kini automatik setiap jam"


else:

    msg = "🌴 Tiada berita FCPO ditemui."


send_telegram(msg)
