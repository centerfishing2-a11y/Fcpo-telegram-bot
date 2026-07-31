import json


def get_technical_data():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "price": "-",
            "daily_trend": "-",
            "h4_trend": "-",
            "h1_trend": "-",
            "support": "-",
            "resistance": "-"
        }
