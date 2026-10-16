from typing import List, Dict
import requests
import base64
from pathlib import Path

from config import ANKI_CONNECT_URL


def store_media_file(audio_file_path: str, filename: str) -> str:
    """上传音频到当前 Anki 用户的媒体目录，返回实际保存的文件名。"""
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
    response = requests.post(ANKI_CONNECT_URL, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    if result.get("error") is None:
        print(f"Updated note_id={note_id}, field={field_name}, new content={updated_content}")
    else:
        raise RuntimeError(f"Failed to update note_id={note_id}, error={result.get('error')}")
