def analyze_news(news_list):
    text = " ".join(news_list).lower()

    score = 50
    support = []
    pressure = []

    bullish = {
        "rebound": 8,
        "rise": 6,
        "rises": 6,
        "higher": 6,
        "gain": 5,
        "gains": 5,
        "firmer": 8,
        "strong": 6,
        "stronger": 6,
        "optimism": 6,
        "export": 5,
        "biodiesel": 10,
        "tight": 8,
        "tightening": 8,
        "supply": 4,
        "demand": 8,
        "mpob": 4,
        "inventory fall": 12,
        "stocks fall": 12
    }

    bearish = {
        "decline": 8,
        "declines": 8,
        "slip": 6,
        "slipped": 6,
        "fall": 5,
        "falls": 5,
        "drop": 5,
        "lower": 5,
        "weak": 6,
        "weaken": 6,
        "weakened": 6,
        "pressure": 5,
        "tariff": 5,
        "inventory rise": 10,
        "stocks rise": 10,
        "oversupply": 10
    }

    for k, v in bullish.items():
        if k in text:
            score += v

    for k, v in bearish.items():
        if k in text:
            score -= v

    if "export" in text:
        support.append("Prospek eksport memberi sokongan kepada FCPO")

    if "biodiesel" in text:
        support.append("Permintaan biodiesel menyokong penggunaan minyak sawit")

    if "firmer" in text or "stronger" in text:
        support.append("Pasaran minyak sayuran menunjukkan pengukuhan")

    if "rebound" in text:
        support.append("Harga sedang menunjukkan pemulihan")

    if "tight" in text or "tightening" in text:
        support.append("Bekalan semakin ketat")

    if "demand" in text:
        support.append("Permintaan kekal positif")

    if "slip" in text or "decline" in text:
        pressure.append("Harga mengalami tekanan penurunan")

    if "weaken" in text or "weakened" in text:
        pressure.append("Pasaran luar sedang melemah")

    if "tariff" in text:
        pressure.append("Isu tarif menambah ketidaktentuan pasaran")

    if "inventory rise" in text:
        pressure.append("Inventori meningkat")

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
        "support": list(dict.fromkeys(support)),
        "pressure": list(dict.fromkeys(pressure))
    }
