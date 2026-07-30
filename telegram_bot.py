import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(message):
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN tidak dijumpai.")
        return False

    if not CHAT_ID:
        print("❌ CHAT_ID tidak dijumpai.")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        r = requests.post(url, data=payload, timeout=20)

        if r.status_code == 200:
            print("✅ Telegram berjaya dihantar.")
            return True
        else:
            print("❌ Telegram gagal dihantar.")
            print(r.text)
            return False

    except Exception as e:
        print(f"❌ Ralat Telegram: {e}")
        return False
