from typing import List, Dict
import requests
import json

ANKI_CONNECT_URL = "http://127.0.0.1:8765"

def get_notes(deck_name: str) -> List[int]:
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {"query": f"deck:{deck_name}"}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    return result.get("result", [])

def get_note_fields(note_id: int) -> Dict:
    payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {"notes": [note_id]}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    if result.get("error") is None and result.get("result"):
        return result["result"][0]["fields"]
    return {}

def update_note_field(note_id: int, field_name: str, updated_content: str) -> None:
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
    if result.get("error") is None:
        print(f"Updated note_id={note_id}, field={field_name}, new content={updated_content}")
    else:
        print(f"Failed to update note_id={note_id}, error={result.get('error')}")