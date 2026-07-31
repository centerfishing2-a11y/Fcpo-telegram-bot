def analyze_news(news_list):
    text = " ".join(news_list).lower()

    score = 50
    support = []
    pressure = []

    bullish = {
        "biodiesel": 10,
        "strong demand": 8,
        "higher": 5,
        "rise": 5,
        "gain": 5,
        "up": 3,
        "tight supply": 10,
        "inventory fall": 12,
        "stocks fall": 10,
        "export increase": 8,
        "mpob": 5
    }

    bearish = {
        "decline": 8,
        "fall": 5,
        "drop": 5,
        "lower": 5,
        "weak": 6,
        "weaker": 6,
        "inventory rise": 10,
        "stocks rise": 10,
        "export fall": 8,
        "crude oil weaker": 8
    }

    for word, value in bullish.items():
        if word in text:
            score += value

    for word, value in bearish.items():
        if word in text:
            score -= value

    if "biodiesel" in text:
        support.append("Permintaan biodiesel menyokong penggunaan minyak sawit")

    if "inventory fall" in text or "stocks fall" in text:
        support.append("Inventori sawit dijangka menurun")

    if "tight supply" in text:
        support.append("Bekalan semakin ketat")

    if "strong demand" in text:
        support.append("Permintaan pasaran kekal kukuh")

    if "export increase" in text:
        support.append("Eksport meningkat")

    if "inventory rise" in text or "stocks rise" in text:
        pressure.append("Inventori meningkat")

    if "export fall" in text:
        pressure.append("Eksport menurun")

    if "crude oil weaker" in text:
        pressure.append("Harga minyak mentah melemah")

    if "decline" in text or "drop" in text:
        pressure.append("Tekanan penurunan harga")

    score = max(0, min(score, 100))

    if score >= 70:
        sentiment = "🟢 BULLISH"
        bias = "BUY ketika retracement"

    elif score <= 35:
        sentiment = "🔴 BEARISH"
        bias = "SELL ketika rebound"

    else:
        sentiment = "🟡 NEUTRAL"
        bias = "Tunggu pengesahan arah"

    return {
        "score": score,
        "sentiment": sentiment,
        "bias": bias,
        "support": support,
        "pressure": pressure
    }
