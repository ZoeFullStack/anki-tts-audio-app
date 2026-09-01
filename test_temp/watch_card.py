import requests
import time
import re


def get_current_card():
    """
    获取当前 Anki 卡片信息

    返回
    dict 卡片数据，失败返回 None
    """
    try:
        r = requests.post("http://127.0.0.1:8765", json={
            "action": "guiCurrentCard",
            "version": 6
        }, timeout=2)
        return r.json().get("result")
    except Exception:
        return None


def strip_html(text):
    """
    移除 HTML 标签

    参数
    text: 含 HTML 的字符串

    返回
    纯文本字符串
    """
    return re.sub(r'<[^>]+>', '', text).strip()


def main():
    """
    主循环：轮询 AnkiConnect，检测卡片变化并输出到控制台
    """
    last_card_id = None
    last_shown = None

    print("监听 Anki 卡片... (Ctrl+C 退出)\n")

    while True:
        card = get_current_card()

        if card:
            card_id = card.get("cardId")
            # 有 buttons 代表已翻牌显示背面
            shown = "answer" if card.get("buttons") else "question"

            if card_id != last_card_id or shown != last_shown:
                last_card_id = card_id
                last_shown = shown

                if shown == "question":
                    content = strip_html(card.get("question", ""))
                    print(f"[正面]\n{content}\n")
                else:
                    content = strip_html(card.get("answer", ""))
                    print(f"[背面]\n{content}\n")

        time.sleep(0.5)


if __name__ == "__main__":
    main()
