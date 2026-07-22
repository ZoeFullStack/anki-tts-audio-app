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
