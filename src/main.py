# Entry point that generates Anki TTS audio. Scope: generate_audio_filename, get_tts_params, process_field_pair, generate_and_store_audio, print_progress, main.

import os
import time
from tempfile import TemporaryDirectory

from anki_utils import get_note_fields, get_notes_from_decks, store_media_file, update_note_field
from audio_compat import ensure_mobile_compatible_audio, with_converted_suffix
from config import (
    DECK_NAMES,
    FIELD_MAPPINGS,
    SKIP_EXISTING_AUDIO,
    TTS_ENGINE,
    TTS_LANGUAGE_CONFIG,
    TTS_REQUEST_SLEEP,
)
from language_utils import detect_language, normalize_tts_text, strip_html
from tts_utils import text_to_speech


# Build a safe Anki media filename from text and language.
def generate_audio_filename(text: str, lang: str) -> str:
    clean_text = text.strip()[:15]
    replacements = {
        "\\": "＼",
        "/": "／",
        ":": "：",
        "*": "＊",
        "?": "？",
        '"': "＂",
        "<": "＜",
        ">": "＞",
        "|": "｜",
        " ": "_",
    }
    for char, replacement in replacements.items():
        clean_text = clean_text.replace(char, replacement)

    engine_suffix = TTS_ENGINE.lower()
    timestamp = int(time.time()) % 10000
    return f"{clean_text}_{lang}_{engine_suffix}_{timestamp}_local.mp3"


# Return gTTS/Edge voice params for a language.
def get_tts_params(lang: str) -> tuple[str, str]:
    cfg = TTS_LANGUAGE_CONFIG[lang]
    if TTS_ENGINE.lower() == "edge":
        return cfg["gtts_lang"], cfg["edge_voice"]
    return cfg["gtts_lang"], cfg["gtts_tld"]


# Generate audio for one source field and write it to the target field.
def process_field_pair(note_id: int, fields: dict, source_field: str, target_field: str) -> bool:
    raw_value = fields.get(source_field, {}).get("value", "")
    text_to_convert = normalize_tts_text(strip_html(raw_value))

    existing_audio = fields.get(target_field, {}).get("value", "").strip()

    if not text_to_convert:
        return False

    if existing_audio and SKIP_EXISTING_AUDIO:
        print(
            f"Skipping note ID {note_id} [{source_field}->{target_field}] "
            f"- already has audio: {existing_audio}"
        )
        return False

    lang = detect_language(text_to_convert)
    print(
        f"Processing note ID {note_id} [{source_field}->{target_field}] "
        f"detected={lang}, text={text_to_convert[:30]}"
    )
    try:
        audio_file_name = generate_and_store_audio(text_to_convert, lang)
        anki_sound_format = f"[sound:{audio_file_name}]"
        update_note_field(note_id, target_field, anki_sound_format)
        print(f"Updated note ID {note_id} with audio file: {anki_sound_format}")
        time.sleep(TTS_REQUEST_SLEEP)
        return True
    except Exception as e:
        print(f"Skip failed note ID {note_id} [{source_field}->{target_field}]: {e}")
        return False


# Create mobile-playable audio and store it in Anki media.
def generate_and_store_audio(text: str, lang: str) -> str:
    lang_code, voice = get_tts_params(lang)
    audio_file_name = generate_audio_filename(text, lang)
    with TemporaryDirectory(prefix="anki-tts-") as temp_dir:
        audio_file_path = os.path.join(temp_dir, "audio.mp3")
        text_to_speech(
            text=text,
            audio_file_path=audio_file_path,
            lang=lang_code,
            engine=TTS_ENGINE,
            voice=voice,
        )
        audio_file_path = ensure_mobile_compatible_audio(audio_file_path)
        audio_file_name = with_converted_suffix(audio_file_name, audio_file_path)
        return store_media_file(audio_file_path, audio_file_name)


# Print how much of the batch is done.
def print_progress(done: int, total: int) -> None:
    if total <= 0:
        return
    percent = done * 100 // total
    filled = percent // 2
    bar = "#" * filled + "-" * (50 - filled)
    print(f"Progress [{bar}] {percent}% ({done}/{total})", flush=True)


# Process every mapped field on notes from DECK_NAMES.
def main():
    note_ids = get_notes_from_decks(DECK_NAMES)
    total = len(note_ids) * len(FIELD_MAPPINGS)
    done = 0
    print_progress(done, total)
    for note_id in note_ids:
        fields = get_note_fields(note_id)
        for mapping in FIELD_MAPPINGS:
            process_field_pair(
                note_id,
                fields,
                mapping["source"],
                mapping["target"],
            )
            done += 1
            print_progress(done, total)


if __name__ == "__main__":
    main()
