# Poll AnkiConnect and print the current card front/back. Scope: get_current_card, strip_html, main.

import requests
import time
import re


# Get the card currently being reviewed.
def get_current_card():
    try:
        r = requests.post("http://127.0.0.1:8765", json={
            "action": "guiCurrentCard",
            "version": 6
        }, timeout=2)
        return r.json().get("result")
    except Exception:
        return None


# Strip HTML tags from card content.
def strip_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()


# Watch for card changes and print question/answer text.
def main():
    last_card_id = None
    last_shown = None

    print("Listening for Anki cards... (Ctrl+C to quit)\n")

    while True:
        card = get_current_card()

        if card:
            card_id = card.get("cardId")
            shown = "answer" if card.get("buttons") else "question"

            if card_id != last_card_id or shown != last_shown:
                last_card_id = card_id
                last_shown = shown

                if shown == "question":
                    content = strip_html(card.get("question", ""))
                    print(f"[Front]\n{content}\n")
                else:
                    content = strip_html(card.get("answer", ""))
                    print(f"[Back]\n{content}\n")

        time.sleep(0.5)


if __name__ == "__main__":
    main()
