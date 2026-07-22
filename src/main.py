import os
import time

from anki_utils import get_note_fields, get_notes, update_note_field
from config import (
    AUDIO_OUTPUT_DIR,
    DECK_NAME,
    FIELD_MAPPINGS,
    TTS_ENGINE,
    TTS_LANGUAGE_CONFIG,
)
from language_utils import detect_language
from tts_utils import text_to_speech


def generate_audio_filename(text: str, lang: str) -> str:
    """
    根据文本内容生成音频文件名

    参数
    text: 源文本
    lang: 语言代码

    返回
    str: 音频文件名
    """
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


def get_tts_params(lang: str) -> tuple[str, str]:
    """
    根据语言和引擎获取 TTS 参数

    参数
    lang: 语言代码 'ja' 或 'en'

    返回
    tuple[str, str]: (语言代码, voice 或 tld)
    """
    cfg = TTS_LANGUAGE_CONFIG[lang]
    if TTS_ENGINE.lower() == "edge":
        return cfg["gtts_lang"], cfg["edge_voice"]
    return cfg["gtts_lang"], cfg["gtts_tld"]


def process_field_pair(note_id: int, fields: dict, source_field: str, target_field: str) -> bool:
    """
    处理单个字段映射：读取源字段并生成目标音频

    参数
    note_id: Anki 笔记 ID
    fields: 笔记字段字典
    source_field: 源文字段名
    target_field: 目标音频字段名

    返回
    bool: 是否成功生成并更新
    """
    text_to_convert = fields.get(source_field, {}).get("value", "").strip()
    existing_audio = fields.get(target_field, {}).get("value", "").strip()

    if not text_to_convert:
        return False

    if existing_audio:
        print(
            f"Skipping note ID {note_id} [{source_field}->{target_field}] "
            f"- already has audio: {existing_audio}"
        )
        return False

    lang = detect_language(text_to_convert)
    lang_code, voice = get_tts_params(lang)
    audio_file_name = generate_audio_filename(text_to_convert, lang)
    audio_file_path = os.path.join(AUDIO_OUTPUT_DIR, audio_file_name)

    print(
        f"Processing note ID {note_id} [{source_field}->{target_field}] "
        f"detected={lang}, text={text_to_convert[:30]}"
    )

    text_to_speech(
        text=text_to_convert,
        audio_file_path=audio_file_path,
        lang=lang_code,
        engine=TTS_ENGINE,
        voice=voice,
    )

    anki_sound_format = f"[sound:{audio_file_name}]"
    update_note_field(note_id, target_field, anki_sound_format)
    print(f"Updated note ID {note_id} with audio file: {anki_sound_format}")
    return True


def main():
    """
    批量处理 Anki 笔记的多组字段 TTS 生成

    参数
    无

    返回
    无
    """
    note_ids = get_notes(DECK_NAME)
    for note_id in note_ids:
        fields = get_note_fields(note_id)
        for mapping in FIELD_MAPPINGS:
            process_field_pair(
                note_id,
                fields,
                mapping["source"],
                mapping["target"],
            )


if __name__ == "__main__":
    main()
