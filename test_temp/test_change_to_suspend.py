import requests

# AnkiConnect 地址
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# 在这里设置要处理的牌组名。当前有效牌组是 speak，english/japanese 已不存在。
DECK_NAMES = ["speak"]
EASY_EASE = 4
MIN_EASY_STREAK = 7

# 获取指定牌组中的所有卡片
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

# 获取卡片的复习记录
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

# 获取卡片的详细信息，包括 noteId
def get_card_info(card_ids):
    payload = {
        "action": "cardsInfo",
        "version": 6,
        "params": {"cards": card_ids}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None:
        return result["result"]  # 返回卡片的详细信息列表
    else:
        print("Error:", result.get("error"))
        return []

# 使用 areSuspended 方法筛选非暂停状态的卡片
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
        suspended_status = result["result"]  # 返回一个布尔值列表
        non_suspended_cards = [
            card_id for card_id, is_suspended in zip(card_ids, suspended_status) if not is_suspended
        ]
        return non_suspended_cards
    else:
        print("Error:", result.get("error"))
        return []

# 将符合条件的卡片设置为暂停状态
def suspend_cards(card_ids):
    """
    暂停指定卡片

    参数
    card_ids: 卡片 ID 列表

    返回
    无
    """
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


def count_consecutive_easy(review_list, ease=EASY_EASE):
    """
    统计连续选 Easy 的最长次数

    参数
    review_list: 单张卡片的复习记录
    ease: Anki 按钮值，4 表示 Easy

    返回
    int: 最长连续 Easy 次数
    """
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


def filter_easy_cards(deck_name, min_streak=MIN_EASY_STREAK):
    """
    筛选连续选 Easy 达到阈值、且尚未暂停的卡片

    参数
    deck_name: 牌组名
    min_streak: 连续 Easy 最少次数

    返回
    tuple[list, list]: (noteId 列表, cardId 列表)
    """
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
