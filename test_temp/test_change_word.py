from googletrans import Translator
import requests
import re
import json
import os
import concurrent.futures

ANKI_CONNECT_URL = "http://127.0.0.1:8765"
DECK_NAME = "N1-2"
CACHE_FILE = "translation_cache.json"

# SOURCE_FIELD = "VocabKanji"    # 日语字段名
# TARGET_FIELD = "VocabDefEN"    # 英语字段名

SOURCE_FIELD = "SentKanji1"    # 日语字段名
TARGET_FIELD = "SentEN"    # 英语字段名

# 加载翻译缓存
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        translation_cache = json.load(f)
else:
    translation_cache = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(translation_cache, f, ensure_ascii=False, indent=2)

def mymemory_translate(text):
    if text in translation_cache:
        return translation_cache[text]
    for attempt in range(3):
        try:
            resp = requests.get(
                "https://api.mymemory.translated.net/get",
                params={"q": text, "langpair": "ja|en"},
                timeout=10
            )
            print(f"[DEBUG] MyMemory response for '{text}': {resp.text}")  # 增加调试输出
            if resp.status_code == 200:
                data = resp.json()
                translated = data.get("responseData", {}).get("translatedText", "")
                translation_cache[text] = translated
                save_cache()
                return translated
        except Exception as e:
            print(f"[DEBUG] Exception: {e}")
    return ""

def get_cards_by_deck(deck_name):
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {"query": f"deck:{deck_name}"}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    return result.get("result", [])

def get_card_fields(note_id):
    payload = {"action": "notesInfo", "version": 6, "params": {"notes": [note_id]}}
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None and result.get("result"):
        return result["result"][0]["fields"]
    return {}

def update_card_field(note_id, field_name, updated_content):
    payload = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": {
                    field_name: updated_content
                },
            }
        },
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    print(f"Update response: {result}")
    if result.get("error") is None:
        print(f"更新成功: note_id={note_id}, 字段={field_name}, 新内容={updated_content}")
    else:
        print(f"更新失败: note_id={note_id}, 错误={result.get('error')}")

def batch_translate_and_update(deck_name, source_field, target_field, batch_size=50):
    note_ids = get_cards_by_deck(deck_name)
    # 先筛选需要处理的note_id
    notes_to_process = []
    for note_id in note_ids:
        fields = get_card_fields(note_id)
        jp_text = fields.get(source_field, {}).get("value", "")
        target_text = fields.get(target_field, {}).get("value", "")
        if jp_text.strip() and not target_text.strip():
            notes_to_process.append(note_id)
    total = len(notes_to_process)
    print(f"总共需要处理的 note 数量: {total}")

    for start in range(0, total, batch_size):
        batch_note_ids = notes_to_process[start:start+batch_size]
        texts_to_translate = []
        note_ids_to_update = []

        # 收集本批需要翻译的内容和对应的 note_id
        for note_id in batch_note_ids:
            fields = get_card_fields(note_id)
            jp_text = fields.get(source_field, {}).get("value", "")
            target_text = fields.get(target_field, {}).get("value", "")
            if jp_text.strip() and not target_text.strip():
                texts_to_translate.append(jp_text)
                note_ids_to_update.append(note_id)

        print(f"本批需要翻译的数量: {len(texts_to_translate)}")

        # 并发翻译
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            translated_list = list(executor.map(mymemory_translate, texts_to_translate))

        # 更新到目标字段
        for nid, en_text, jp_text in zip(note_ids_to_update, translated_list, texts_to_translate):
            update_card_field(nid, target_field, en_text)
            print(f"已更新 note id: {nid}，{source_field}: {jp_text} -> {target_field}: {en_text}")

if __name__ == "__main__":
    batch_translate_and_update(DECK_NAME, SOURCE_FIELD, TARGET_FIELD, batch_size=100)