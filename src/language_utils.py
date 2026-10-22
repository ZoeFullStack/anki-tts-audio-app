# Text cleanup and language helpers for TTS. Scope: normalize_tts_text, strip_html, build_ssml, detect_language.

import html
import re

JAPANESE_PATTERN = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]")


# Normalize apostrophes and HTML entities so English contractions read correctly.
def normalize_tts_text(text: str) -> str:
    for _ in range(3):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded
    text = re.sub(r"(?<=[A-Za-z])[‘’ʼ＇`´](?=[A-Za-z])", "'", text)
    return text.strip()


# Strip HTML tags from Anki field text.
def strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text).strip()


# Build Edge TTS SSML and replace noisy punctuation with pauses.
def build_ssml(text: str, voice: str) -> str:
    text = text.replace("<", "").replace(">", "")
    text = re.sub(r"[/\\|_]", " ", text)
    text = re.sub(r"[(){}\[\]#*~`^@]", "", text)
    text = re.sub(r" +", " ", text).strip()
    text = re.sub(r"[!！?？;；]", '<break time="200ms"/>', text)
    text = text.replace("&", "&amp;")

    xml_lang = "-".join(voice.split("-")[:2])
    return (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xml:lang="{xml_lang}">'
        f'<voice name="{voice}">{text}</voice></speak>'
    )


# Detect Japanese vs English from the source text.
def detect_language(text: str) -> str:
    clean = strip_html(text)
    if not clean:
        return "en"
    if JAPANESE_PATTERN.search(clean):
        return "ja"
    return "en"
