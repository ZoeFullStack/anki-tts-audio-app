from anki_utils import get_notes, get_note_fields,update_note_field
from tts_utils import text_to_speech
from config import (
    ANKI_CONNECT_URL, DECK_NAME, SOURCE_FIELD, TARGET_FIELD, AUDIO_OUTPUT_DIR,
    TTS_ENGINE, EDGE_TTS_VOICE, GTTS_LANGUAGE, GTTS_TLD
)
import os
import re
import time

def generate_audio_filename(text: str) -> str:
    """
    Generate a descriptive filename for the audio file based on the text content.
    Format: [first few characters of text]_[engine]_[timestamp].mp3
    
    For Japanese text, this will create filenames like:
    おす_オス━_edge_1234_local.mp3
    """
    # Clean the text - keep only first few characters (up to 15) for filename
    # For Japanese text, each character is meaningful, so we keep more characters
    clean_text = text.strip()[:15]
    
    # Replace problematic characters for filenames
    # Windows filename restrictions: \ / : * ? " < > |
    replacements = {
        '\\': '＼', '/': '／', ':': '：', '*': '＊', 
        '?': '？', '"': '＂', '<': '＜', '>': '＞', 
        '|': '｜', ' ': '_'
    }
    
    for char, replacement in replacements.items():
        clean_text = clean_text.replace(char, replacement)
    
    # Add engine type and timestamp to make filename unique
    engine_suffix = TTS_ENGINE.lower()
    timestamp = int(time.time()) % 10000  # Last 4 digits of timestamp for uniqueness
    
    # Create filename in the requested format
    filename = f"{clean_text}_{engine_suffix}_{timestamp}_local.mp3"
    
    return filename

def main():
    note_ids = get_notes(DECK_NAME)
    for note_id in note_ids:
        fields = get_note_fields(note_id)
        text_to_convert = fields.get(SOURCE_FIELD, {}).get("value", "")
        
        if text_to_convert:
            audio_file_name = generate_audio_filename(text_to_convert)
            audio_file_path = os.path.join(AUDIO_OUTPUT_DIR, audio_file_name)
            
            # Select appropriate parameters based on the engine
            voice = None
            lang = GTTS_LANGUAGE  # Default to configured language
            
            if TTS_ENGINE.lower() == 'edge':
                voice = EDGE_TTS_VOICE
            elif TTS_ENGINE.lower() == 'gtts':
                voice = GTTS_TLD  # For gTTS, we'll use the voice parameter to pass the TLD
            
            # Call text_to_speech with the appropriate parameters
            text_to_speech(
                text=text_to_convert, 
                audio_file_path=audio_file_path,
                lang=lang,
                engine=TTS_ENGINE,
                voice=voice
            )
            
            # Format the audio file reference in Anki sound format: [sound:filename.mp3]
            anki_sound_format = f"[sound:{audio_file_name}]"
            update_note_field(note_id, TARGET_FIELD, anki_sound_format)
            print(f"Updated note ID {note_id} with audio file: {anki_sound_format}")

if __name__ == "__main__":
    main()