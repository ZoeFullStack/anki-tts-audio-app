# Export selected Anki fields as CSV lines. Scope: get_cards_by_deck, get_card_info.

import requests

# AnkiConnect endpoint.
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# Target deck name.
DECK_NAME = "N1"  # Replace with the real deck name

# Find card IDs in one deck.
def get_cards_by_deck(deck_name):
    payload = {
        "action": "findCards",
        "version": 6,
        "params": {"query": f"deck:{deck_name}"}
    }q
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        return result.get("result", [])
    else:
        print("Error:", result.get("error"))
        return []

# Fetch card details including fields.
def get_card_info(card_ids):
    payload = {
        "action": "cardsInfo",
        "version": 6,
        "params": {"cards": card_ids}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        return result["result"]
    else:
        print("Error:", result.get("error"))
        return []

if __name__ == "__main__":
    card_ids = get_cards_by_deck(DECK_NAME)
    if not card_ids:
        print("No cards found")
        exit()

    card_info_list = get_card_info(card_ids)

    print("Card fields (one card per line, comma-separated):")
    for card_info in card_info_list:
        word = card_info.get("fields").get("Word").get("value")
        explain1 = card_info.get("fields").get("Explain1").get("value")
        connectiveType1 = card_info.get("fields").get("ConnectiveType1").get("value")
        

        print(f"{word},{explain1},{connectiveType1}")