from anki_utils import get_notes, get_note_fields,update_note_field
from tts_utils import text_to_speech
from config import ANKI_CONNECT_URL, DECK_NAME, SOURCE_FIELD, TARGET_FIELD, AUDIO_OUTPUT_DIR
import hashlib
import os

def generate_audio_filename(text: str) -> str:
    hash_object = hashlib.sha256(text.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    return f"{hex_dig}.mp3"

def main():
    note_ids = get_notes(DECK_NAME)
    for note_id in note_ids:
        fields = get_note_fields(note_id)
        text_to_convert = fields.get(SOURCE_FIELD, {}).get("value", "")

        if text_to_convert:
            audio_file_name = generate_audio_filename(text_to_convert)
            audio_file_path = os.path.join(AUDIO_OUTPUT_DIR, audio_file_name)
            success = text_to_speech(text_to_convert, audio_file_path)
            if success:
                update_note_field(note_id, TARGET_FIELD, audio_file_name)
                print(f"Updated note ID {note_id} with audio file: {audio_file_name}")
            else:
                print(f"Failed to generate audio for note ID {note_id}")

if __name__ == "__main__":
    main()