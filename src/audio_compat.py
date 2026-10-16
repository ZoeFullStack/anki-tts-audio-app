import shutil
import subprocess
from pathlib import Path


def with_converted_suffix(filename: str, converted_path: str) -> str:
    """
    把原始文件名后缀改成转换后的音频格式

    参数
    filename: 计划上传到 Anki 的文件名
    converted_path: 转换后的本地文件路径

    返回
    str: 与转换结果一致后缀的文件名
    """
    return Path(filename).with_suffix(Path(converted_path).suffix).name


def ensure_mobile_compatible_audio(audio_file_path: str) -> str:
    """
    将 TTS 音频转为手机 Anki 可播放的 m4a

    参数
    audio_file_path: 原始音频路径

    返回
    str: 转换后的文件路径；无法转换时返回原路径
    """
    src = Path(audio_file_path)
    if not src.exists() or src.stat().st_size == 0:
        raise RuntimeError(f"Audio file missing or empty: {audio_file_path}")

    dst = src.with_suffix(".m4a")
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        _run_converter(
            [ffmpeg, "-y", "-i", str(src), "-c:a", "aac", "-b:a", "64k", str(dst)]
        )
        return str(dst)

    afconvert = shutil.which("afconvert")
    if afconvert:
        _run_converter([afconvert, "-f", "m4af", "-d", "aac", str(src), str(dst)])
        return str(dst)

    print(
        "Warning: ffmpeg/afconvert not found. "
        "gTTS MP3 often fails on AnkiMobile; install ffmpeg to convert."
    )
    return str(src)


def _run_converter(cmd: list[str]) -> None:
    """
    执行音频转换命令并检查输出文件

    参数
    cmd: 转换命令参数列表

    返回
    无
    """
    dst = Path(cmd[-1])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not dst.exists() or dst.stat().st_size == 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"Audio convert failed: {' '.join(cmd)}\n{detail}")
    print(f"Converted to mobile-compatible audio: {dst}")
