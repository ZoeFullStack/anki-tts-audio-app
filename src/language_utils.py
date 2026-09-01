import re

JAPANESE_PATTERN = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]")


def strip_html(text: str) -> str:
    """
    去除 HTML 标签

    参数
    text: 原始文本

    返回
    str: 纯文本
    """
    return re.sub(r"<[^>]+>", "", text).strip()


def build_ssml(text: str, voice: str) -> str:
    """
    将文本转为 Edge TTS SSML 格式，避免标点/特殊符号被读出

    参数
    text: 原始文本（已去除 HTML）
    voice: Edge TTS 声音名，如 'ja-JP-NanamiNeural'

    返回
    str: 完整 SSML 字符串
    """
    text = text.replace("<", "").replace(">", "")           # 清除残留 HTML
    text = re.sub(r"[/\\|_]", " ", text)                   # 分隔符 → 空格（须在 SSML 注入前，防止破坏 />）
    text = re.sub(r"[(){}\[\]#*~`^@]", "", text)           # 无意义符号移除，保留内容
    text = re.sub(r" +", " ", text).strip()
    text = re.sub(r"[!！?？;；]", '<break time="200ms"/>', text)  # 句末标点 → 停顿
    text = text.replace("&", "&amp;")                      # & 转义须最后，防止 &amp; 的 ; 被上行误判

    # 从 voice 提取 xml:lang（'ja-JP-NanamiNeural' → 'ja-JP'）
    xml_lang = "-".join(voice.split("-")[:2])
    return (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xml:lang="{xml_lang}">'
        f'<voice name="{voice}">{text}</voice></speak>'
    )


def detect_language(text: str) -> str:
    """
    检测文本语言（日语或英语）

    参数
    text: 待检测文本

    返回
    str: 'ja' 或 'en'
    """
    clean = strip_html(text)
    if not clean:
        return "en"
    if JAPANESE_PATTERN.search(clean):
        return "ja"
    return "en"
