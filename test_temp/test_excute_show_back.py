# Watch the current Anki card and print back-side fields. Scope: get_current_card, clear_console.

import json
import requests
import time
import os

# Connect to AnkiConnect while Anki is running.
ANKI_CONNECT_URL = "http://127.0.0.1:8765"

# Get the card currently being reviewed.
def get_current_card():
    payload = {
        "action": "guiCurrentCard",
        "version": 6
    }
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        if "result" in result and result["result"]:
            return result["result"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to AnkiConnect: {e}")
        return None

# Clear the terminal on Windows or Unix.
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    last_card_id = None
    while True:
        current_card = get_current_card()
        if current_card:
            current_card_id = current_card.get("cardId")
            if current_card_id != last_card_id:
                last_card_id = current_card_id
                clear_console()

                back_value = current_card.get("fields", {}).get("背面", {}).get("value")
                sentence = current_card.get("fields", {}).get("sentence", {}).get("value")
                VocabKanji = current_card.get("fields", {}).get("backMeaning", {}).get("value")
                Example1 = current_card.get("fields", {}).get("Example1", {}).get("value")
                meaning = current_card.get("fields", {}).get("meaning", {}).get("value")
                output = ""
                if back_value:
                    output += back_value
                    output +=  '\n'
                if sentence:
                    output += sentence
                if meaning:
                    output += meaning
                elif VocabKanji: 
                    output = (
                        current_card.get("fields", {}).get("backMeaning", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("frontSentence", {}).get("value", "")
                    )
                    print(output)
                elif meaning:
                    output = (
                        current_card.get("fields", {}).get("grammer", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("connect", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("sentence", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("meaning", {}).get("value", "")
                    )
                    print(output) 
                elif Example1:
                    output = (
                        current_card.get("fields", {}).get("Word", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Explain1", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese1", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Example1", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese1", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Example2", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese2", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Example3", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese3", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Example4", {}).get("value", "") + '\n' +
                        current_card.get("fields", {}).get("Chinese4", {}).get("value", "") 
                    )
                    print(output)  
                print(output)
        else:
            print("can't find this test")

        time.sleep(0.5)
