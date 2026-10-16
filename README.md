# anki-tts-audio-app

## Overview
The anki-tts-audio-app is a Python application designed to integrate with Anki, a popular flashcard application. This project fetches text from Anki notes, converts it to speech using a free text-to-speech (TTS) service, and saves the generated audio files back to specified fields in Anki.

## Features
- Fetch text from Anki notes.
- Convert text to speech using a free TTS service.
- Save audio files back to Anki notes.
- Easy configuration for Anki API and TTS settings.

## Project Structure
```
anki-tts-audio-app
├── src
│   ├── main.py          # Entry point of the application
│   ├── tts_utils.py     # Utility functions for TTS conversion
│   ├── anki_utils.py     # Functions to interact with Anki
│   └── config.py        # Configuration settings
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/anki-tts-audio-app.git
   cd anki-tts-audio-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration
Before running the application, you may need to configure the `src/config.py` file to set the Anki API URL and the fields used for text and audio.

### 音频存储（Windows / macOS / Linux）

打开 Anki 并安装、启用 AnkiConnect，切换到需要处理的 Anki 用户。
在 `src/config.py` 中设置 `DECK_NAME` 和 `FIELD_MAPPINGS`；本机默认接口为 `http://127.0.0.1:8765`。

无需设置 `collection.media` 的绝对路径或相对路径。程序先在系统临时目录生成 MP3，
再通过 AnkiConnect 的 `storeMediaFile` 接口存入当前用户的媒体目录，成功后写入
`[sound:实际文件名]`，并自动清理临时文件。同名文件不会被覆盖。
项目目录的相对路径并不等于 Anki 的媒体目录，因此仅把旧路径改成 `./audio` 无法让 Anki 正常读取音频。

已有内容的音频字段仍会跳过，此改动不会自动迁移旧电脑的音频或修复已有的失效引用。
运行期间请保持同一个 Anki 用户处于打开状态。

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
