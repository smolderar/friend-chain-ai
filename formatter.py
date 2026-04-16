def detect_emoji(title):
    t = title.lower()

    if "hack" in t or "exploit" in t or "risk" in t:
        return "⚠️"
    elif "airdrop" in t or "reward" in t or "campaign" in t:
        return "🪂"
    elif "trend" in t or "viral" in t or "heating" in t:
        return "🔥"
    elif "etf" in t or "market" in t or "volume" in t:
        return "📊"
    else:
        return "🚨"

def make_why_it_matters(title):
    t = title.lower()

    if "hack" in t or "exploit" in t:
        return "Security events can hit confidence fast."

    if "listing" in t:
        return "Listings often bring attention and volatility."

    if "airdrop" in t:
        return "Early participation can matter if ecosystems grow."

    if "etf" in t:
        return "Regulatory moves often impact market sentiment."

    if "partnership" in t:
        return "Strong partnerships can expand real adoption."

    return "This could matter if momentum continues."

def make_watch(title):
    t = title.lower()

    if "hack" in t:
        return "Official response and fund safety updates."

    if "listing" in t:
        return "Volume and price reaction after launch."

    if "airdrop" in t:
        return "Eligibility rules and deadlines."

    if "etf" in t:
        return "Market reaction in the next sessions."

    return "Whether this grows or fades next."

def format_post(item):
    title = item["title"]
    source = item["source"]
    link = item["link"]

    emoji = detect_emoji(title)
    why = make_why_it_matters(title)
    watch = make_watch(title)

    msg = f"""{emoji} {title}

What happened:
{title}

Why it matters:
{why}

What to watch:
{watch}

Source:
{source}
{link}
"""
    return msg

def format_recap(items):
    lines = ["📌 Daily Crypto Recap\n"]

    for i, item in enumerate(items[:5], start=1):
        lines.append(f"{i}. {item['title']}")

    lines.append("\nStay sharp.")
    return "\n".join(lines)