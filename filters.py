import re

HIGH_PRIORITY = [
    "hack", "exploit", "etf", "listing", "launch",
    "airdrop", "partnership", "approval", "binance",
    "coinbase", "breaking", "solana", "ethereum"
]

MEDIUM_PRIORITY = [
    "update", "trend", "growth", "volume",
    "users", "campaign", "reward", "ecosystem"
]

LOW_QUALITY = [
    "price prediction", "100x", "moon", "lambo",
    "sponsored", "shill", "giveaway"
]

TRUSTED_SOURCES = [
    "cointelegraph",
    "coindesk",
    "decrypt",
    "cryptopotato",
    "binance",
    "coinbase",
    "x trends"
]

def normalize(text):
    return text.lower().strip()

def trust_score(source):
    s = normalize(source)
    score = 0

    for item in TRUSTED_SOURCES:
        if item in s:
            score += 3

    return score

def priority_score(title):
    t = normalize(title)
    score = 0

    for word in HIGH_PRIORITY:
        if word in t:
            score += 5

    for word in MEDIUM_PRIORITY:
        if word in t:
            score += 2

    for bad in LOW_QUALITY:
        if bad in t:
            score -= 10

    return score

def is_useful(title):
    score = priority_score(title)
    return score > 0

def remove_duplicates(items):
    seen = set()
    clean = []

    for item in items:
        key = normalize(item["title"])

        if key not in seen:
            seen.add(key)
            clean.append(item)

    return clean

def rank_items(items):
    ranked = []

    for item in items:
        total = trust_score(item["source"]) + priority_score(item["title"])

        item["score"] = total

        if total >= 3:
            ranked.append(item)

    ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)
    return ranked

def get_best_items(items, limit=5):
    items = remove_duplicates(items)
    items = rank_items(items)
    return items[:limit]