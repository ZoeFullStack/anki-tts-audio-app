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

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.