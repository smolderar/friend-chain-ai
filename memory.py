import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "sent_titles": [],
            "today_posts": []
        }

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {
            "sent_titles": [],
            "today_posts": []
        }

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def already_sent(title):
    data = load_memory()
    return title.lower() in [x.lower() for x in data["sent_titles"]]

def mark_sent(title):
    data = load_memory()

    if title not in data["sent_titles"]:
        data["sent_titles"].append(title)

    if title not in data["today_posts"]:
        data["today_posts"].append(title)

    save_memory(data)

def get_today_posts():
    data = load_memory()
    return data["today_posts"]

def clear_today_posts():
    data = load_memory()
    data["today_posts"] = []
    save_memory(data)