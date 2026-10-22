# Convert TTS audio to a mobile-playable format. Scope: with_converted_suffix, ensure_mobile_compatible_audio, _run_converter.

import shutil
import subprocess
from pathlib import Path


# Keep the Anki filename suffix in sync with the converted file.
def with_converted_suffix(filename: str, converted_path: str) -> str:
    return Path(filename).with_suffix(Path(converted_path).suffix).name


# Convert TTS audio to m4a so AnkiMobile can play it.
def ensure_mobile_compatible_audio(audio_file_path: str) -> str:
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


# Run ffmpeg/afconvert and verify the output file.
def _run_converter(cmd: list[str]) -> None:
    dst = Path(cmd[-1])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or not dst.exists() or dst.stat().st_size == 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(f"Audio convert failed: {' '.join(cmd)}\n{detail}")
    print(f"Converted to mobile-compatible audio: {dst}")
