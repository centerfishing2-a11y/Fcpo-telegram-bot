from datetime import datetime, timezone, timedelta

from news import get_fcpo_news
from analysis import analyze_news
from telegram_bot import send_telegram


def malaysia_time():
    return (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%d-%m-%Y %H:%M")


def build_report(news, result):
    report = f"""🌴 <b>LAPORAN FUNDAMENTAL FCPO</b>

📅 {malaysia_time()} MYT

━━━━━━━━━━━━━━━━━━

📰 <b>BERITA UTAMA</b>

"""

    if news:
        for item in news:
            report += f"• {item}\n\n"
    else:
        report += "Tiada berita utama ditemui.\n\n"

    report += f"""━━━━━━━━━━━━━━━━━━

📊 <b>SENTIMEN PASARAN</b>

{result['sentiment']}
Skor : {result['score']}/100

Bias :
{result['bias']}

━━━━━━━━━━━━━━━━━━

🟢 <b>FAKTOR SOKONGAN</b>

"""

    if result["support"]:
        for s in result["support"]:
            report += f"✅ {s}\n"
    else:
        report += "• Tiada faktor sokongan utama.\n"

    report += "\n🔴 <b>FAKTOR TEKANAN</b>\n\n"

    if result["pressure"]:
        for p in result["pressure"]:
            report += f"⚠️ {p}\n"
    else:
        report += "• Tiada faktor tekanan utama.\n"

    report += "\n━━━━━━━━━━━━━━━━━━\n\n"

    report += "🎯 <b>KESIMPULAN TRADER</b>\n\n"

    if result["score"] >= 70:
        report += "Fundamental lebih memihak kepada BUY."

    elif result["score"] <= 35:
        report += "Fundamental lebih memihak kepada SELL."

    else:
        report += "Fundamental masih bercampur. Tunggu pengesahan arah."

    report += "\n\n🤖 FCPO BOT PRO V2"

    return report


def main():
    news = get_fcpo_news()

    result = analyze_news(news)

    report = build_report(news, result)

    send_telegram(report)


if __name__ == "__main__":
    main()
