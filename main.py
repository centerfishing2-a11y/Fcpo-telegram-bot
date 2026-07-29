import os
import requests
import feedparser
from urllib.parse import quote
from datetime import datetime, timezone, timedelta

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram(msg):
    if not BOT_TOKEN or not CHAT_ID:
        print("Ralat: BOT_TOKEN atau CHAT_ID tiada dalam tetapan GitHub Secrets!")
        return
        
    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })
    if response.status_code == 200:
        print("Mesej berjaya dihantar ke Telegram.")
    else:
        print(f"Gagal hantar ke Telegram: {response.text}")

def get_news():
    q = quote("FCPO palm oil Malaysia biodiesel MPOB export inventory")
    url = f"https://google.com{q}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        feed = feedparser.parse(response.content)
    except Exception as e:
        print(f"Ralat ambil data dari Google News: {e}")
        return []

    result = []
    blacklist = [
        "indicator", "signal", "calendar", "history", 
        "course", "explained"
    ]

    if not hasattr(feed, 'entries') or not feed.entries:
        print("Tiada sebarang artikel ditemui dalam RSS Google News.")
        return []

    # --- KOD UJIAN (PILIHAN 1): MATIKAN TAPISAN MASA ---
    # Kita ambil terus 5 berita teratas yang ada di Google News tanpa mengira masa ia diterbitkan
    for item in feed.entries[:20]:
        title = getattr(item, 'title', '')
        if not title:
            continue
            
        low = title.lower()
        if any(x in low for x in blacklist):
            continue

        # Masukkan terus tanpa tapisan masa had_masa
        result.append(title)
        if len(result) == 5:
            break

    return result


def analysis(news):
    if not news:
        return "🟡 NEUTRAL", 50, "Tunggu pengesahan arah", [], []
        
    text = " ".join(news).lower()
    bull = []
    bear = []
    score = 50

    if any(x in text for x in ["stocks expected to fall", "inventory fall", "stocks drop"]):
        score += 15
        bull.append("Inventori sawit dijangka menurun, memberi sokongan kepada harga")

    if any(x in text for x in ["supply outlook tightens", "tightening supply", "less supply"]):
        score += 15
        bull.append("Bekalan semakin ketat dan boleh menyokong kenaikan FCPO")

    if "biodiesel" in text:
        score += 10
        bull.append("Permintaan biodiesel meningkatkan penggunaan sawit")

    if "price expected" in text:
        score += 5
        bull.append("Unjuran harga masih menunjukkan sokongan")

    if any(x in text for x in ["exports fall", "export decline", "lower exports"]):
        score -= 10
        bear.append("Eksport menurun memberi tekanan kepada permintaan")

    if any(x in text for x in ["crude oil weaken", "weaker crude", "brent drop"]):
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

# --- Aliran Utama Yang Dilindungi (Protected Main Flow) ---
if __name__ == "__main__":
    try:
        news = get_news()

        if news:
            sent, score, bias, bull, bear = analysis(news)
            waktu_malaysia = datetime.now(timezone.utc) + timedelta(hours=8)
            
            msg = (
                "🌴 LAPORAN FUNDAMENTAL FCPO\n"
                f"📅 {waktu_malaysia.strftime('%d-%m-%Y %H:%M')} (MYT)\n\n"
                "━━━━━━━━━━━━━━\n\n"
                "📰 BERITA UTAMA\n\n"
            )

            for n in news:
                msg += "• " + n + "\n\n"

            msg += (
                "━━━━━━━━━━━━━━\n\n"
                "📊 SENTIMEN PASARAN FCPO\n\n"
                f"Sentimen: {sent}\n"
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

            msg += "\n━━━━━━━━━━━━━━\n\n🎯 KESIMPULAN TRADER\n\n"

            if score >= 65:
                msg += "Fundamental lebih menyokong kenaikan FCPO."
            elif score <= 35:
                msg += "Tekanan fundamental masih menguasai FCPO."
            else:
                msg += "Fundamental bercampur. Tunggu pengesahan trend."

            msg += "\n\n⏰ Kemas kini automatik setiap jam"
            send_telegram(msg)
        else:
            print("Status: Tiada berita FCPO terbaharu dikesan dalam tempoh 1 jam lepas. Aliran selesai dengan selamat.")
            
    except Exception as utama_error:
        print(f"SISTEM DIKESAN RALAT: {utama_error}")
