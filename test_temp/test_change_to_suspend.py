# Suspend cards with 7+ consecutive Easy(4) reviews. Scope: get_cards_by_deck, get_reviews_of_cards, get_card_info, filter_non_suspended_cards, suspend_cards, count_consecutive_easy, filter_easy_cards.

import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from config import ANKI_CONNECT_URL, DECK_NAMES

EASY_EASE = 4
MIN_EASY_STREAK = 7


# Find card IDs in one deck.
def get_cards_by_deck(deck_name):
    payload = {
        "action": "findCards",
        "version": 6,
        "params": {"query": f'deck:"{deck_name}"'}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        return result.get("result", [])
    else:
        print("Error:", result.get("error"))
        return []


# Fetch review history for a list of cards.
def get_reviews_of_cards(card_ids):
    payload = {
        "action": "getReviewsOfCards",
        "version": 6,
        "params": {"cards": card_ids}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        return result["result"]
    else:
        print("Error:", result.get("error"))
        return {}


# Fetch card details including note IDs.
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


# Keep only cards that are not already suspended.
def filter_non_suspended_cards(card_ids):
    if not card_ids:
        return []
    payload = {
        "action": "areSuspended",
        "version": 6,
        "params": {"cards": card_ids}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        suspended_status = result["result"]
        non_suspended_cards = [
            card_id for card_id, is_suspended in zip(card_ids, suspended_status) if not is_suspended
        ]
        return non_suspended_cards
    else:
        print("Error:", result.get("error"))
        return []


# Suspend the given cards.
def suspend_cards(card_ids):
    if not card_ids:
        print("no cards to suspend")
        return
    payload = {
        "action": "suspend",
        "version": 6,
        "params": {"cards": card_ids}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        print(f"suspend success CardId: {card_ids}")
    else:
        print("Error:", result.get("error"))


# Return the longest consecutive Easy streak on one card.
def count_consecutive_easy(review_list, ease=EASY_EASE):
    review_list.sort(key=lambda x: x["id"])
    max_streak = 0
    current_streak = 0
    for review in review_list:
        if review.get("ease") == ease:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return max_streak


# Find unsuspended cards whose Easy streak meets the threshold.
def filter_easy_cards(deck_name, min_streak=MIN_EASY_STREAK):
    card_ids = list(map(int, get_cards_by_deck(deck_name)))
    if not card_ids:
        print(f"no cards in deck: {deck_name}")
        return [], []
    easy_cards = []
    reviews = get_reviews_of_cards(card_ids)
    for card_id, review_list in reviews.items():
        streak = count_consecutive_easy(review_list)
        if streak >= min_streak:
            easy_cards.append(int(card_id))
            print(f"match card={card_id} easy_streak={streak}")

    non_suspended_cards = filter_non_suspended_cards(easy_cards)
    card_info_list = get_card_info(non_suspended_cards)
    note_ids = [card_info["note"] for card_info in card_info_list]
    return note_ids, non_suspended_cards

if __name__ == "__main__":
    for deck_name in DECK_NAMES:
        print(f"process deck: {deck_name}")
        print("filtering consecutive Easy(4) >= 7 ...")
        note_ids, card_ids = filter_easy_cards(deck_name)
        print("matched note ids:")
        for note_id in note_ids:
            print(note_id)
        print("suspending cards...")
        suspend_cards(card_ids)
