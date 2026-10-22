# AnkiConnect helpers for notes and media. Scope: store_media_file, get_notes, get_notes_from_decks, get_note_fields, update_note_field.

from typing import List, Dict
import requests
import base64
from pathlib import Path

from config import ANKI_CONNECT_URL


# Upload a local audio file into the current Anki media folder.
def store_media_file(audio_file_path: str, filename: str) -> str:
    data = base64.b64encode(Path(audio_file_path).read_bytes()).decode("ascii")
    response = requests.post(
        ANKI_CONNECT_URL,
        json={
            "action": "storeMediaFile",
            "version": 6,
            "params": {"filename": filename, "data": data, "deleteExisting": False},
        },
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()
    if result.get("error") is not None:
        raise RuntimeError(f"Failed to store media: {result['error']}")
    stored_filename = result.get("result")
    if not isinstance(stored_filename, str) or not stored_filename:
        raise RuntimeError("AnkiConnect did not return a media filename")
    return stored_filename


# Find note IDs in one deck.
def get_notes(deck_name: str) -> List[int]:
    escaped_deck_name = deck_name.replace('"', r'\"')
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {"query": f'deck:"{escaped_deck_name}"'}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload)
    result = response.json()
    return result.get("result", [])


# Collect unique note IDs from multiple decks.
def get_notes_from_decks(deck_names: List[str]) -> List[int]:
    note_ids = []
    seen = set()
    for deck_name in deck_names:
        ids = get_notes(deck_name)
        print(f"deck={deck_name} notes={len(ids)}")
        for note_id in ids:
            if note_id in seen:
                continue
            seen.add(note_id)
            note_ids.append(note_id)
    return note_ids


# Read all fields of one note.
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


# Write one note field through AnkiConnect.
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
    response = requests.post(ANKI_CONNECT_URL, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    if result.get("error") is None:
        print(f"Updated note_id={note_id}, field={field_name}, new content={updated_content}")
    else:
        raise RuntimeError(f"Failed to update note_id={note_id}, error={result.get('error')}")
