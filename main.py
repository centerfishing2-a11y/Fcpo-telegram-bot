from datetime import datetime, timezone, timedelta

from news import get_fcpo_news
from analysis import analyze_news
from telegram_bot import send_telegram
from technical import get_technical_data


def malaysia_time():
    return (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%d-%m-%Y %H:%M")


def build_report(news, result, technical):
    report = f"""🌴 <b>FCPO PRO REPORT V4</b>

📅 {malaysia_time()} MYT

━━━━━━━━━━━━━━━━━━

💰 <b>PASARAN FCPO</b>

Harga Semasa : <b>{technical['price']}</b>

📈 Trend Daily : {technical['daily_trend']}

📈 Trend H4 : {technical['h4_trend']}

📈 Trend H1 : {technical['h1_trend']}

🟢 Support : {technical['support']}

🔴 Resistance : {technical['resistance']}

━━━━━━━━━━━━━━━━━━

📰 <b>BERITA UTAMA</b>

"""

    for i, item in enumerate(news, start=1):
        report += f"{i}. {item}\n\n"
    
    report += "━━━━━━━━━━━━━━━━━━\n\n"

    report += "🟢 <b>FAKTOR SOKONGAN</b>\n\n"

    if result["support"]:
        for s in result["support"]:
            report += f"✅ {s}\n"
    else:
        report += "• Tiada faktor sokongan utama.\n"

    report += "\n"

    report += "🔴 <b>FAKTOR TEKANAN</b>\n\n"

    if result["pressure"]:
        for p in result["pressure"]:
            report += f"⚠️ {p}\n"
    else:
        report += "• Tiada faktor tekanan utama.\n"

    report += "\n━━━━━━━━━━━━━━━━━━\n\n"

    report += "📝 <b>RUMUSAN FUNDAMENTAL</b>\n\n"

    if result["score"] >= 70:
        report += (
            "Sentimen fundamental lebih memihak kepada kenaikan harga FCPO. "
            "Permintaan dan faktor sokongan pasaran masih mengatasi tekanan semasa.\n\n"
        )

    elif result["score"] <= 35:
        report += (
            "Sentimen fundamental lebih cenderung negatif. "
            "Trader perlu berhati-hati kerana tekanan pasaran masih tinggi.\n\n"
        )

    else:
        report += (
            "Sentimen pasaran masih bercampur. "
            "Terdapat faktor positif yang menyokong harga, namun risiko luaran masih wujud. "
            "Pergerakan harga dijangka bergantung kepada perkembangan berita seterusnya.\n\n"
        )

    report += "━━━━━━━━━━━━━━━━━━\n\n"

    report += "🎯 <b>KESIMPULAN TRADER</b>\n\n"

    if result["score"] >= 70:
        report += "🟢 Bias: BUY ketika retracement."

    elif result["score"] <= 35:
        report += "🔴 Bias: SELL ketika rebound."

    else:
        report += "🟡 Bias: Tunggu pengesahan arah sebelum membuat entry."

    report += "\n\n━━━━━━━━━━━━━━━━━━"

    report += "\n🤖 FCPO BOT PRO V3"

    return report


def main():
    news = get_fcpo_news()

    result = analyze_news(news)

    technical = get_technical_data()

    report = build_report(news, result, technical)

    send_telegram(report)


if __name__ == "__main__":
    main()
